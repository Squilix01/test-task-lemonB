from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SalesHistoryCreate(BaseModel):
    name: str
    category: str
    price: float
    rating: Optional[float] = 0
    number_of_reviews: Optional[int] = 0
    product_url: Optional[str] = ""
    image_url: Optional[str] = ""
    keywords: Optional[str] = ""


class SalesHistoryResponse(BaseModel):
    id: int
    name: str
    category: str
    price: float
    rating: Optional[float]
    number_of_reviews: Optional[int]
    product_url: Optional[str]
    image_url: Optional[str]
    keywords: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class SalesHistoryListResponse(BaseModel):
    items: list[SalesHistoryResponse]
    total: int
