from py.database import *
from fastapi import Depends, FastAPI, Body
from fastapi import Response
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
import jwt
from jose.exceptions import JWTError 
from sqlalchemy.exc import IntegrityError
import os
from sqlalchemy.future import select
from fastapi import Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware



Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "http://localhost",
    "http://127.0.0.1"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SECRET_KEY = "rupollyalalalallai3yr273hfcqaid12ufdwd9q39hfge"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 160

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, password):
    return pwd_context.verify(plain_password, password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# авторизация пользователя
@app.post("/users/login", summary="Авторизация пользователя", tags=["Пользователи"])
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Авторизует пользователя, возвращает токен доступа.
    - **login**: логин пользователя
    - **password**: пароль пользователя
    """ 
    user = db.query(UserDB).filter(UserDB.login == form_data.username).first()

    # проверяем
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный номер телефона или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": str(user.user_id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# регистрация пользователя
@app.post(
    "/user/registration", summary="Регистрация пользователя", tags=["Пользователи"]
)
async def registration_new_user(user_data: User, db: Session = Depends(get_db)):
    """
    - **login**: уникальный логин
    - **password**: пароль пользователя
    """
    # проверяем, существует ли пользователь с таким логином
    existing_user = db.query(UserDB).filter(UserDB.login == user_data.login).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким логином уже существует",
        )

    # хешируем пароль
    hashed_password = get_password_hash(user_data.password)

    # создаем нового пользователя
    new_user = UserDB(login=user_data.login, password=hashed_password)

    db.add(new_user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Ошибка при добавлении пользователя"
        )

    return {"message": "Пользователь добавлен"}


# Функция для получения задач пользователя
def get_tasks_by_user(db, user_id: int):
    return db.query(Task).filter(Task.user_id == user_id).all()


# Получение задач определенного юзера
@app.get("/task/user/task_all", response_model=List[TaskResponse], summary="Получить задачи пользователя", tags=["Задачи"])
async def get_tasks(request: Request, db: Session = Depends(get_db)):
    """
    Возвращает все задачи определенного пользователя.
    Требуется аутентификация пользователя по login в токене.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = request.cookies.get("users_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось подтвердить учетные данные",
        )

    # Декодирование JWT токена
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось подтвердить учетные данные",
        )
    # token = request.headers.get("Authorization")
    # if token is None or not token.startswith("Bearer "):
    #     raise credentials_exception
    # token = token[7:]

    # try:
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #     user_id: str = payload.get("sub")
    #     if user_id is None:
    #         raise credentials_exception
    # except JWTError as e:
    #     print(f"JWT Error: {e}")
    #     raise credentials_exception

    # Получаем задачи пользователя
    tasks = get_tasks_by_user(db, int(user_id))

    # Преобразуем каждый объект Task в TaskResponse с помощью from_orm
    return [TaskResponse.from_orm(task) for task in tasks]

@app.post("/task/create", summary="Создать задачу для опредленного пользователя", tags=["Задачи"])
async def create_task(
    request: Request, task: TaskCreate, db: Session = Depends(get_db)
):
    """
    Создает и добавляет задачу для определенного пользователя.
    Требуется аутентификация пользователя по login в токене.

    Поля для добавления задачи:
    - **title**: Название задачи
    - **deadline**: Дата завершения задачи
    - **completed**: Статус задачи
    - **importance**: Важность задачи
    """
    print(f"Received task data: {task}")
    token = request.cookies.get("users_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось подтвердить учетные данные",
        )

    # Декодирование JWT токена
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось подтвердить учетные данные",
        )
    # credentials_exception = HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Не удалось подтвердить учетные данные",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )

    # token = request.headers.get("Authorization")
    # if token is None or not token.startswith("Bearer "):
    #     raise credentials_exception
    # token = token[7:]

    # try:
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #     user_id: str = payload.get("sub")
    #     if user_id is None:
    #         raise credentials_exception
    # except JWTError as e:
    #     print(f"JWT Error: {e}")
    #     raise credentials_exception

    try:
        new_task = Task(
            user_id=user_id,
            createdAt=datetime.utcnow(),
            importance=task.importance,
            completed=task.completed,
            title=task.title,
            deadline=task.deadline,
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        print(f"Создана задача: {new_task}")
        db.close()
        return new_task
    finally:
        db.close()

class TaskUpdate(BaseModel):
    completed: bool

@app.put("/task/{task_id}/update")
async def update_task(task_id: int,task_update: TaskUpdate,request: Request,db: Session = Depends(get_db)):
    token = request.cookies.get("users_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось подтвердить учетные данные",
        )

    # Декодирование JWT токена
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось подтвердить учетные данные",
        )
    # credentials_exception = HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Не удалось подтвердить учетные данные",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )
    
    # token = request.headers.get("Authorization")
    # print(f"Received Token: {token}")
    # if token is None or not token.startswith("Bearer "):
    #     raise credentials_exception
    # token = token[7:]

    # try:
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #     user_id: str = payload.get("sub")
    #     print(f"Decoded user_id: {user_id}")
    #     if user_id is None:
    #         raise credentials_exception
    # except JWTError as e:
    #     print(f"JWT Error: {e}")
    #     raise credentials_exception
    
    # task = db.query(Task).filter(Task.task_id == task_id).first()
    # if task.user_id != user_id:
    #     print(f"User {user_id} is not authorized to modify task {task_id}")
    #     raise HTTPException(status_code=403, detail="У вас нет разрешения на изменение этой задачи")
    user_id = int(payload.get("sub"))
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if not isinstance(user_id, int) or not isinstance(task.user_id, int):
       raise HTTPException(status_code=400, detail="Неверный формат идентификатора пользователя")
    print(f"Task user_id: {task.user_id}")
    print(f"Current user_id from token: {user_id}")
    print(f"Task user_id from database: {task.user_id}")

    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="У вас нет разрешения на изменение этой задачи")

    task.completed = task_update.completed
    db.commit()
    db.refresh(task)
    return task

# # удаление задачи
@app.delete("/task/delete/{task_id}", summary="Удалить задачу опредленного пользователя", tags=["Задачи"])
async def task_delete(task_id: int, request: Request, db: Session = Depends(get_db)):
    """
    Удаляет задачу определенного пользователя.
    Требуется аутентификация пользователя по login в токене.
    """

    token = request.cookies.get("users_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось подтвердить учетные данные",
        )

    # Декодирование JWT токена
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось подтвердить учетные данные",
        )

    # credentials_exception = HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Не удалось подтвердить учетные данные",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )
    
    # token = request.headers.get("Authorization")
    # print(f"Received Token: {token}")
    # if token is None or not token.startswith("Bearer "):
    #     raise credentials_exception
    # token = token[7:]

    # try:
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #     user_id: str = payload.get("sub")
    #     print(f"Decoded user_id: {user_id}")
    #     if user_id is None:
    #         raise credentials_exception
    # except JWTError as e:
    #     print(f"JWT Error: {e}")
    #     raise credentials_exception
    
    

    db = SessionLocal()
    try:
        task = (
            db.query(Task)
            .filter(Task.task_id == task_id, Task.user_id == user_id)
            .first()
        )
        if task is None:
            return JSONResponse(
                status_code=404, content={"message": "Задача не найдена."}
            )

        # 
        print(f"Task found: {task}")
        db.delete(task)
        db.commit()

         
        return {"message": "Задача удалена."}
    finally:
        db.close()

@app.put("/task/editing/{task_id}", response_model=TaskResponse, summary="Обновить информацию о задачи по ее ID", tags=["Задачи"])
async def update_task(
    task_id: int,
    request: Request,
    task_update: TaskCreate,
    db: Session = Depends(get_db),
):
    """
    Обновляет информацию о задаче по её ID.
    Требуется аутентификация пользователя по login в токене.

    Поля для обновления задачи:
    - **title**: Основной текст задачи
    - **important**: Важность задачи
    - **completed**: Статус задачи
    """
    token = request.cookies.get("users_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось подтвердить учетные данные",
        )

    # Декодирование JWT токена
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось подтвердить учетные данные",
        )
    # credentials_exception = HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Не удалось подтвердить учетные данные",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )
    
    # token = request.headers.get("Authorization")
    # print(f"Received Token: {token}")
    # if token is None or not token.startswith("Bearer "):
    #     raise credentials_exception
    # token = token[7:]

    # try:
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #     user_id: str = payload.get("sub")
    #     print(f"Decoded user_id: {user_id}")
    #     if user_id is None:
    #         raise credentials_exception
    # except JWTError as e:
    #     print(f"JWT Error: {e}")
    #     raise credentials_exception
    
    
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    # Обновляем поля задачи
    task.title = task_update.title
    task.deadline = task_update.deadline
    task.importance = task_update.importance
    task.completed = task_update.completed

    db.commit()
    db.refresh(task)

    return task

