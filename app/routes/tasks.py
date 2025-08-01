from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional

from app.schemas import TarefaBase, TarefaOut
from app.database import get_db
from app.security import get_current_user
from app.repositories import (
    create_tarefa, get_tarefas_by_user, get_tarefa, update_tarefa, delete_tarefa
)
from app.models import Tarefa

router = APIRouter()

@router.post("/", response_model=TarefaOut)
def criar_tarefa(
    tarefa: TarefaBase,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Cria uma nova tarefa para o usuário autenticado.

    Args:
        tarefa (TarefaBase): Dados da tarefa.
        db (Session): Sessão do banco de dados.
        current_user (Usuario): Usuário autenticado.

    Returns:
        TarefaOut: Dados da tarefa criada.
    """
    return create_tarefa(db, tarefa, current_user.id)


@router.get("/", response_model=List[TarefaOut])
def listar_tarefas(
    status: Optional[str] = None,
    prioridade: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Lista todas as tarefas do usuário autenticado com filtros opcionais.

    Args:
        status (str, optional): Filtro pelo status da tarefa.
        prioridade (str, optional): Filtro pela prioridade.
        db (Session): Sessão do banco de dados.
        current_user (Usuario): Usuário autenticado.

    Returns:
        List[TarefaOut]: Lista de tarefas encontradas.
    """
    return get_tarefas_by_user(db, current_user.id, status, prioridade)


@router.get("/{tarefa_id}", response_model=TarefaOut)
def obter_tarefa(
    tarefa_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Recupera uma tarefa específica do usuário autenticado.

    Args:
        tarefa_id (UUID): ID da tarefa.
        db (Session): Sessão do banco de dados.
        current_user (Usuario): Usuário autenticado.

    Returns:
        TarefaOut: Dados da tarefa encontrada.

    Raises:
        HTTPException: Se a tarefa não for encontrada.
    """
    tarefa = get_tarefa(db, tarefa_id, current_user.id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa


@router.put("/{tarefa_id}", response_model=TarefaOut)
def atualizar_tarefa(
    tarefa_id: UUID,
    tarefa_data: TarefaBase,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Atualiza os dados de uma tarefa do usuário autenticado.

    Args:
        tarefa_id (UUID): ID da tarefa.
        tarefa_data (TarefaBase): Dados atualizados.
        db (Session): Sessão do banco de dados.
        current_user (Usuario): Usuário autenticado.

    Returns:
        TarefaOut: Tarefa atualizada.

    Raises:
        HTTPException: Se a tarefa não for encontrada.
    """
    tarefa = get_tarefa(db, tarefa_id, current_user.id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return update_tarefa(db, tarefa, tarefa_data)


@router.delete("/{tarefa_id}")
def deletar_tarefa(
    tarefa_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Remove uma tarefa do usuário autenticado.

    Args:
        tarefa_id (UUID): ID da tarefa.
        db (Session): Sessão do banco de dados.
        current_user (Usuario): Usuário autenticado.

    Returns:
        dict: Confirmação de exclusão.

    Raises:
        HTTPException: Se a tarefa não for encontrada.
    """
    tarefa = get_tarefa(db, tarefa_id, current_user.id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    delete_tarefa(db, tarefa)
    return {"ok": True}


@router.post("/{tarefa_id}/complete", response_model=TarefaOut)
def concluir_tarefa(
    tarefa_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Marca uma tarefa como concluída.

    Args:
        tarefa_id (UUID): ID da tarefa.
        db (Session): Sessão do banco de dados.
        current_user (Usuario): Usuário autenticado.

    Returns:
        TarefaOut: Tarefa atualizada como concluída.

    Raises:
        HTTPException: Se a tarefa não for encontrada.
    """
    tarefa = get_tarefa(db, tarefa_id, current_user.id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    tarefa.status = "concluida"
    db.commit()
    db.refresh(tarefa)
    return tarefa
