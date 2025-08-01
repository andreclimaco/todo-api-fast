from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from uuid import uuid4
from sqlalchemy.orm import Session

from app.schemas import UserCreate, Token, UserOut
from app.security import get_password_hash, verify_password, create_access_token, oauth2_scheme, get_current_user
from app.repositories import get_user_by_email, create_user
from app.models import Usuario
from app.database import get_db

router = APIRouter()

@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Cria um novo usuário e retorna um token JWT.

    Args:
        user (UserCreate): Objeto com nome, email e senha fornecidos pelo usuário.
        db (Session): Sessão do banco de dados.

    Returns:
        Token: Token JWT de acesso válido por 24h.
    """
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="E-mail já registrado")

    senha_hash = get_password_hash(user.senha)
    novo_usuario = create_user(db, user, senha_hash)

    access_token = create_access_token(
        data={"sub": str(novo_usuario.id)},
        expires_delta=timedelta(minutes=60 * 24)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Realiza login de um usuário válido e retorna um token JWT.

    Args:
        form_data (OAuth2PasswordRequestForm): Contém os campos username (email) e password.
        db (Session): Sessão do banco de dados.

    Returns:
        Token: Token JWT de acesso.
    """
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=60 * 24)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
def obter_usuario_atual(current_user: Usuario = Depends(get_current_user)):
    """
    Retorna os dados do usuário autenticado.

    Args:
        current_user (Usuario): Usuário autenticado via token JWT.

    Returns:
        UserOut: Dados públicos do usuário.
    """
    return current_user  # ✅ FastAPI converte automaticamente para UserOut

