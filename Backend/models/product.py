from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy import String, Integer, Float, Text, CheckConstraint, DateTime, func
from models.base import Base
from datetime import datetime


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    category: Mapped[str] = mapped_column(String(200), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    number_of_reviews: Mapped[int] = mapped_column(Integer, nullable=False)
    product_url: Mapped[str] = mapped_column(String, nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=False)

    score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    reasoning: Mapped[str | None] = mapped_column(Text, nullable=True)
    trend_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    boost_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"Product(id={self.id}, name={self.name}, score={self.score})"

    @validates("name")
    def validate_name(self, key, value: str) -> str:
        if not value:
            raise ValueError("Назва продукту не може бути пустою.")
        if len(value) < 3:
            raise ValueError("Назва продукту повинна містити принаймні 3 символи.")
        return value

    @validates("price")
    def validate_price(self, key, value: float) -> float:
        if value < 0:
            raise ValueError("Ціна не може бути від'ємною.")
        return value

    @validates("rating")
    def validate_rating(self, key, value: float) -> float:
        if value < 0 or value > 5:
            raise ValueError("Рейтинг повинен бути в межах від 0 до 5.")
        return value

    @validates("number_of_reviews")
    def validate_number_of_reviews(self, key, value: int) -> int:
        if value < 0:
            raise ValueError("Кількість відгуків не може бути від'ємною.")
        return value

    __table_args__ = (
        CheckConstraint('price >= 0', name='check_price_non_negative'),
        CheckConstraint('rating >= 0 AND rating <= 5', name='check_rating_range'),
        CheckConstraint('number_of_reviews >= 0', name='check_reviews_non_negative'),
        CheckConstraint('score >= 0 AND score <= 100', name='check_score_range'),
    )