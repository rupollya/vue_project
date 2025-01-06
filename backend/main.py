from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from py.database import Base, engine
from auth import router as auth_router
from tasks import router as tasks_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Manager",
    version="1.0.0",
    docs_url="/docs", 
    openapi_url="/openapi.json" 
)

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:80",
    "http://77.222.43.163:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

app.include_router(auth_router, prefix="/auth", tags=["Авторизация"])
app.include_router(tasks_router, prefix="/tasks", tags=["Задачи"])

