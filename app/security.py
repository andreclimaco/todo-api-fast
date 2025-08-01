# app/security.py

import os
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories import get_user_by_id
from app.models import Usuario

# Configurações do JWT
SECRET_KEY = os.getenv("SECRET_KEY", "chave-secreta-super-segura")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas

# Configuração de criptografia de senha com Bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 usando Bearer Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_password_hash(password: str) -> str:
    """
    Gera o hash de uma senha utilizando bcrypt.

    Args:
        password (str): Senha em texto plano.

    Returns:
        str: Hash da senha.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha corresponde ao hash armazenado.

    Args:
        plain_password (str): Senha fornecida pelo usuário.
        hashed_password (str): Hash armazenado no banco.

    Returns:
        bool: True se a senha for válida, False caso contrário.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Gera um token JWT com os dados fornecidos.

    Args:
        data (dict): Dados que serão codificados no token (ex: {"sub": user_id}).
        expires_delta (Optional[timedelta]): Tempo de expiração. Padrão: 24h.

    Returns:
        str: Token JWT codificado.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    """
    Recupera o usuário autenticado com base no token JWT.

    Args:
        token (str): Token JWT enviado no header Authorization.
        db (Session): Sessão ativa do banco de dados.

    Returns:
        Usuario: Instância do usuário autenticado.

    Raises:
        HTTPException: Se as credenciais forem inválidas ou token estiver expirado/malformado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_id(db, UUID(user_id))
    if user is None:
        raise credentials_exception

    return user
