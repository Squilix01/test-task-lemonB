import asyncio
import pytest
from services.scoring.ai_scorer import ProductScorer
from services.scoring.boost import BoostCalculator


class FakeSalesRepo:
    def __init__(self, data):
        self.data = data

    async def get_all(self, skip=0, limit=1000):
        return self.data


class FakeSalesItem:
    def __init__(self, name, category, rating, reviews, keywords):
        self.name = name
        self.category = category
        self.rating = rating
        self.number_of_reviews = reviews
        self.keywords = keywords


@pytest.mark.asyncio
async def test_fallback_scoring_without_ai():
    """Тест математичного скорингу згідно з формулою ТЗ без підключення LLM."""
    scorer = ProductScorer()
    # Ensure no LLM keys are used
    scorer.api_key = ""
    scorer.llm_provider = ""

    # Товар з високими метриками: рейтинг 5.0, відгуків 2000, тренд 80, буст 10
    # Очікуємо: (5/5)*25 + min(2000/1000, 1)*25 + 80*0.25 + 10 = 25 + 25 + 20 + 10 = 80
    score, reasoning = await scorer.calculate_score(
        name="Test Wireless Earbuds",
        category="Electronics",
        rating=5.0,
        reviews=2000,
        trend_score=80.0,
        boost_score=10.0,
    )

    assert score == 80
    assert "Формула ТЗ (без AI)" in reasoning
    assert "Підсумок: 80/100" in reasoning


@pytest.mark.asyncio
async def test_boost_calculator_keyword_matching():
    """Тест розрахунку бонусних балів на основі історії продажів."""
    mock_history = [
        FakeSalesItem(
            name="Apple AirPods Pro",
            category="Electronics",
            rating=4.8,
            reviews=5000,
            keywords="apple airpods wireless bluetooth earbuds audio",
        )
    ]
    repo = FakeSalesRepo(mock_history)
    calc = BoostCalculator(repo)

    # Перевіряємо товар зі збігом ключових слів
    boost = await calc.calculate(
        category="Electronics",
        keywords=["wireless", "bluetooth", "earbuds"]
    )
    assert boost > 0
    assert boost <= 20.0
