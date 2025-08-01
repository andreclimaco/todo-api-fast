from sqlalchemy.orm import Session
from uuid import UUID
from app.models import Usuario, Tarefa
from app.schemas import UserCreate, TarefaBase
from datetime import datetime

def get_user_by_email(db: Session, email: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.email == email).first()

def get_user_by_id(db: Session, user_id: UUID) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.id == user_id).first()

def create_user(db: Session, user_data: UserCreate, senha_hash: str) -> Usuario:
    usuario = Usuario(
        nome=user_data.nome,
        email=user_data.email,
        senha_hash=senha_hash,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def create_tarefa(db: Session, tarefa_data: TarefaBase, usuario_id: UUID) -> Tarefa:
    tarefa = Tarefa(
        **tarefa_data.dict(),
        dono_id=usuario_id,
        criado_em=datetime.utcnow(),
        atualizada_em=datetime.utcnow()
    )
    db.add(tarefa)
    db.commit()
    db.refresh(tarefa)
    return tarefa

def get_tarefa(db: Session, tarefa_id: UUID, usuario_id: UUID) -> Tarefa | None:
    return db.query(Tarefa).filter(Tarefa.id == tarefa_id, Tarefa.dono_id == usuario_id).first()

def get_tarefas_by_user(db: Session, usuario_id: UUID, status: str = None, prioridade: str = None):
    query = db.query(Tarefa).filter(Tarefa.dono_id == usuario_id)
    if status:
        query = query.filter(Tarefa.status == status)
    if prioridade:
        query = query.filter(Tarefa.prioridade == prioridade)
    return query.all()

def update_tarefa(db: Session, tarefa: Tarefa, tarefa_data: TarefaBase) -> Tarefa:
    for key, value in tarefa_data.dict().items():
        setattr(tarefa, key, value)
    tarefa.atualizada_em = datetime.utcnow()
    db.commit()
    db.refresh(tarefa)
    return tarefa

def delete_tarefa(db: Session, tarefa: Tarefa):
    db.delete(tarefa)
    db.commit()