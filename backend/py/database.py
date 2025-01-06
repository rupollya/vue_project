from sqlalchemy import create_engine, exc, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, timezone
from typing import Union, Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, String, DateTime, ForeignKey
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, timezone
from typing import Union, Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, String, DateTime, ForeignKey
import os


 
data = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", 3306),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "505750"),
    "database": os.getenv("DB_NAME", "task_manager3"),
}

 
engine = create_engine(f"mysql+pymysql://{data['user']}:{data['password']}@{data['host']}:{data['port']}/")

# Создаем базу данных, если она не существует
try:
    with engine.connect() as connection:
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {data['database']};"))
    print(f"База данных {data['database']} успешно создана или уже существует.")
    
except exc.SQLAlchemyError as e:
    print(f"Ошибка при создании базы данных: {e}")


SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{data['user']}:{data['password']}@{data['host']}:{data['port']}/{data['database']}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    login = Column(String(50), unique=True, index=True)   
    password = Column(String(100))   

# Модель SQLAlchemy для задачи
class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True)  
    user_id = Column(Integer, ForeignKey("users.user_id"))
    createdAt = Column(DateTime, default=datetime.utcnow)   
    importance = Column(String(10), default="низкая")
    completed = Column(Boolean, default=False)
    title = Column(String(1000), nullable=True)  
    deadline = Column(String(100), nullable=True)

# Pydantic модель ответа задачи
class TaskResponse(BaseModel):
    task_id: int   
    title: str  
    deadline: Optional[str] = None
    completed: bool
    importance: str
    user_id: Optional[int] = None
    createdAt: datetime   

    class Config:
        orm_mode = True  
        from_attributes = True   


# Pydantic модель для пользователя
class User(BaseModel):
    login: str
    password: str

    class Config:
        orm_mode = True

# Pydantic модель для создания задачи
class TaskCreate(BaseModel):
    title: str
    deadline: Optional[str] = None
    completed: bool = False
    importance: str = "низкая"  
    class Config:
        orm_mode = True

# Настройка сессии SQLAlchemy
SessionLocal = sessionmaker(autoflush=False, bind=engine)

# Создание базы данных и таблиц
try:
    Base.metadata.create_all(bind=engine)
    print("База данных и таблицы успешно созданы.")
except exc.SQLAlchemyError as e:
    print(f"Ошибка при создании базы данных или таблиц: {e}")