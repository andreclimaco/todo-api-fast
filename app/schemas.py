# app/schemas.py

from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional
from enum import Enum


class PrioridadeEnum(str, Enum):
    """Enum para representar o nível de prioridade da tarefa."""
    baixa = "baixa"
    media = "media"
    alta = "alta"


class StatusEnum(str, Enum):
    """Enum para representar o status atual da tarefa."""
    pendente = "pendente"
    em_andamento = "em_andamento"
    concluida = "concluida"


class TarefaBase(BaseModel):
    """
    Representa os dados básicos de uma tarefa (entrada/atualização).

    Atributos:
        titulo (str): Título da tarefa.
        descricao (Optional[str]): Descrição detalhada.
        data_vencimento (Optional[datetime]): Data limite.
        prioridade (PrioridadeEnum): Nível de prioridade.
        status (StatusEnum): Estado atual da tarefa.
    """
    titulo: str
    descricao: Optional[str] = None
    data_vencimento: Optional[datetime] = None
    prioridade: PrioridadeEnum
    status: StatusEnum


class TarefaOut(TarefaBase):
    """
    Representa os dados de saída de uma tarefa.

    Atributos adicionais:
        id (UUID): Identificador único da tarefa.
        dono_id (UUID): ID do usuário dono da tarefa.
        criado_em (datetime): Timestamp de criação.
        atualizada_em (datetime): Timestamp da última atualização.
    """
    id: UUID
    dono_id: UUID
    criado_em: datetime
    atualizada_em: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    """
    Representa os dados de entrada para criação de um usuário.

    Atributos:
        nome (str): Nome completo.
        email (EmailStr): E-mail válido.
        senha (str): Senha em texto plano.
    """
    nome: str
    email: EmailStr
    senha: str


class UserOut(BaseModel):
    """
    Representa os dados públicos de um usuário.

    Atributos:
        id (UUID): Identificador do usuário.
        nome (str): Nome completo.
        email (EmailStr): E-mail do usuário.
        criado_em (datetime): Timestamp de criação.
    """
    id: UUID
    nome: str
    email: EmailStr
    criado_em: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    """
    Representa um token JWT de autenticação.

    Atributos:
        access_token (str): Token de acesso JWT.
        token_type (str): Tipo do token (ex: "bearer").
    """
    access_token: str
    token_type: str
