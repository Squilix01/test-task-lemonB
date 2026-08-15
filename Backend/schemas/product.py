from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProductResponse(BaseModel):
    id: int
    name: str
    category: str
    price: float
    rating: float
    number_of_reviews: int
    product_url: str
    image_url: str
    score: Optional[int] = None
    reasoning: Optional[str] = None
    trend_score: Optional[float] = None
    boost_score: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProductListResponse(BaseModel):
    products: list[ProductResponse]
    total: int
