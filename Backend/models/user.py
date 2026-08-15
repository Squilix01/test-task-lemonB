from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy import String, Integer, DateTime, func
from models.base import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username})"

    @validates("username")
    def validate_username(self, key, value: str) -> str:
        if not value:
            raise ValueError("Username не може бути пустим.")
        if len(value) < 3:
            raise ValueError("Username повинен містити принаймні 3 символи.")
        return value