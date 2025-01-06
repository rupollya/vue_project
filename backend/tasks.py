from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from py.database import SessionLocal, Task
from jose import jwt, JWTError
from datetime import datetime
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from py.database import *
router = APIRouter()

SECRET_KEY = "rupollyalalalallai3yr273hfcqaid12ufdwd9q39hfge"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/user/task_all", response_model=list[TaskResponse], summary="Получить задачи пользователя")
async def get_tasks(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("users_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось подтвердить учетные данные",
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Не удалось подтвердить учетные данные",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось подтвердить учетные данные",
        )
    tasks = db.query(Task).filter(Task.user_id == int(user_id)).all()
    return [TaskResponse.from_orm(task) for task in tasks]

 
@router.post("/task/create", summary="Создать задачу для опредленного пользователя", tags=["Задачи"])
async def create_task(request: Request, task: TaskCreate, db: Session = Depends(get_db)
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

@router.put("/task/{task_id}/update")
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

 
@router.delete("/task/delete/{task_id}", summary="Удалить задачу опредленного пользователя", tags=["Задачи"])
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

@router.put("/task/editing/{task_id}", response_model=TaskResponse, summary="Обновить информацию о задачи по ее ID", tags=["Задачи"])
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


