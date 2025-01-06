from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from py.database import SessionLocal, UserDB
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel

router = APIRouter()

# Конфигурация авторизации
SECRET_KEY = "rupollyalalalallai3yr273hfcqaid12ufdwd9q39hfge"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 160
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

 
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

 
@router.post("/login", summary="Авторизация пользователя")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(UserDB).filter(UserDB.login == form_data.username).first()
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

 
class User(BaseModel):
    login: str
    password: str

@router.post("/registration", summary="Регистрация пользователя")
async def registration_new_user(user_data: User, db: Session = Depends(get_db)):
    existing_user = db.query(UserDB).filter(UserDB.login == user_data.login).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким логином уже существует",
        )

    hashed_password = get_password_hash(user_data.password)
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