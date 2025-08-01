# app/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL do banco de dados - configurável via variável de ambiente
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/tododb")

# Criação do SQLAlchemy Engine
engine = create_engine(DATABASE_URL)

# Fábrica de sessões vinculada ao engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para declaração dos modelos ORM
Base = declarative_base()


def get_db():
    """
    Retorna uma sessão do banco de dados para ser usada com Depends() nas rotas.

    Yields:
        Session: Sessão ativa do SQLAlchemy para executar operações no banco.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
