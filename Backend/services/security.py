from datetime import datetime, timedelta, timezone
from typing import Any
import jwt
from passlib.context import CryptContext
from settings.config import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Хешування відкритого пароля за допомогою bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Перевірка відповідності відкритого пароля збереженому хешу."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str | Any, expires_delta: timedelta | None = None) -> str:
    """Генерація підписаного JWT токена доступу."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=config.jwt.expiry_minutes)

    to_encode = {"sub": str(subject), "exp": expire}
    return jwt.encode(to_encode, config.jwt.secret_key, algorithm=config.jwt.algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    """Декодування та валідація JWT токена."""
    return jwt.decode(
        token,
        config.jwt.secret_key,
        algorithms=[config.jwt.algorithm],
    )
