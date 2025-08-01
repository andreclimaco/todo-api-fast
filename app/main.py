# app/main.py

from fastapi import FastAPI
from app.routes import auth, tasks

app = FastAPI(
    title="TODO API",
    version="1.0",
    description="API de gerenciamento de tarefas com autenticação JWT."
)

# Inclui as rotas de autenticação no prefixo /auth
app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])

# Inclui as rotas de tarefas no prefixo /tasks
app.include_router(tasks.router, prefix="/tasks", tags=["Tarefas"])
