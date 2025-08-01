# app/models.py

from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid

from app.database import Base


class PrioridadeEnum(str, enum.Enum):
    """Enum para os níveis de prioridade da tarefa."""
    baixa = "baixa"
    media = "media"
    alta = "alta"


class StatusEnum(str, enum.Enum):
    """Enum para os status possíveis da tarefa."""
    pendente = "pendente"
    em_andamento = "em_andamento"
    concluida = "concluida"


class Usuario(Base):
    """
    Modelo de usuário do sistema.

    Atributos:
        id (UUID): Identificador único do usuário.
        nome (str): Nome completo do usuário.
        email (str): E-mail único do usuário.
        senha_hash (str): Hash da senha para autenticação.
        criado_em (datetime): Data de criação do usuário.
        tarefas (List[Tarefa]): Lista de tarefas associadas ao usuário.
    """
    __tablename__ = "usuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)

    tarefas = relationship("Tarefa", back_populates="dono")


class Tarefa(Base):
    """
    Modelo de tarefa atribuída a um usuário.

    Atributos:
        id (UUID): Identificador único da tarefa.
        titulo (str): Título da tarefa.
        descricao (str): Descrição detalhada da tarefa.
        data_vencimento (datetime): Data limite para conclusão.
        prioridade (PrioridadeEnum): Prioridade da tarefa.
        status (StatusEnum): Status atual da tarefa.
        criado_em (datetime): Data de criação da tarefa.
        dono_id (UUID): Chave estrangeira para o usuário dono.
        dono (Usuario): Relacionamento com o modelo Usuario.
    """
    __tablename__ = "tarefas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo = Column(String, nullable=False)
    descricao = Column(Text)
    data_vencimento = Column(DateTime)
    prioridade = Column(Enum(PrioridadeEnum), default=PrioridadeEnum.media)
    status = Column(Enum(StatusEnum), default=StatusEnum.pendente)
    criado_em = Column(DateTime, default=datetime.utcnow)

    dono_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    dono = relationship("Usuario", back_populates="tarefas")
    atualizada_em = Column(DateTime, default=datetime.utcnow)
