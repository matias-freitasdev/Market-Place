from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHash, VerifyMismatchError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError

from core.config import settings

ph = PasswordHasher()
bearer_scheme = HTTPBearer()


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        return ph.verify(stored_hash, password)
    except (VerifyMismatchError, InvalidHash):
        return False


def create_access_token(email: str, expires_delta: timedelta | None = None) -> str:
    to_encode: dict[str, Any] = {"sub": email, "token_type": "access"}
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(email: str, expires_delta: timedelta | None = None) -> str:
    to_encode: dict[str, Any] = {"sub": email, "token_type": "refresh"}
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except InvalidTokenError as exc:
        raise ValueError("Token inválido ou expirado") from exc


def verify_access_token(token: str) -> dict[str, Any]:
    payload = decode_token(token)

    if payload.get("token_type") != "access":
        raise ValueError("Token inválido: tipo incorreto")

    email = payload.get("sub")
    if not email:
        raise ValueError("Token inválido: usuário não encontrado no payload")

    return payload


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict[str, Any]:
    try:
        token = credentials.credentials
        return verify_access_token(token)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc