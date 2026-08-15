from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy import String, Integer, Float, Text, DateTime, func
from models.base import Base
from datetime import datetime


class SalesHistory(Base):
    __tablename__ = "sales_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    category: Mapped[str] = mapped_column(String(200), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True, default=0)
    number_of_reviews: Mapped[int | None] = mapped_column(Integer, nullable=True, default=0)
    product_url: Mapped[str | None] = mapped_column(String, nullable=True, default="")
    image_url: Mapped[str | None] = mapped_column(String, nullable=True, default="")
    keywords: Mapped[str | None] = mapped_column(Text, nullable=True, default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"SalesHistory(id={self.id}, name={self.name}, category={self.category})"

    @validates("name")
    def validate_name(self, key, value: str) -> str:
        if not value:
            raise ValueError("Назва продукту не може бути пустою.")
        return value

    @validates("price")
    def validate_price(self, key, value: float) -> float:
        if value < 0:
            raise ValueError("Ціна не може бути від'ємною.")
        return value
