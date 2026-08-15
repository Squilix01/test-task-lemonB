import asyncio
from unittest.mock import AsyncMock
from services.scoring.boost import BoostCalculator
from models.sales_history import SalesHistory


def test_boost_calculator_with_matches():
    mock_repo = AsyncMock()
    mock_repo.search_by_category_or_keywords.return_value = [
        SalesHistory(name="Anker Power Bank", category="Electronics", rating=4.8, number_of_reviews=5000, keywords="anker,powerbank,battery,charger"),
        SalesHistory(name="Sony Wireless Earbuds", category="Electronics", rating=4.7, number_of_reviews=12000, keywords="sony,wireless,earbuds,audio,bluetooth"),
    ]

    calc = BoostCalculator(mock_repo)
    score = asyncio.run(calc.calculate("Electronics", ["sony", "wireless", "bluetooth", "headphones"]))
    assert score > 0, "Boost score should be greater than 0 for matching keywords"
    assert score <= 20.0, "Boost score should not exceed max boost cap (20.0 pts)"


def test_boost_calculator_no_matches():
    mock_repo = AsyncMock()
    mock_repo.search_by_category_or_keywords.return_value = []

    calc = BoostCalculator(mock_repo)
    score = asyncio.run(calc.calculate("Electronics", ["iphone", "case", "silicone"]))
    assert score == 0.0, "Boost score should be 0.0 when no category or keywords match"


if __name__ == "__main__":
    test_boost_calculator_with_matches()
    test_boost_calculator_no_matches()
    print("✅ test_boost.py passed!")
