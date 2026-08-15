import logging
from repository.sales_history_repo import SalesHistoryRepository

logger = logging.getLogger(__name__)

class BoostCalculator:
    def __init__(self, repo: SalesHistoryRepository):
        self.repo = repo

    async def calculate(self, category: str, keywords: list[str]) -> float:
        try:
            history = await self.repo.search_by_category_or_keywords(category, keywords)
            boost_points: float = 0.0
            
            for item in history:
                if (item.rating and item.rating >= 4.0) or (item.number_of_reviews and item.number_of_reviews >= 100):
                    boost_points += 2.0
            
            if boost_points > 20.0:
                boost_points = 20.0
                
            return boost_points
        except Exception as e:
            logger.error(f"Помилка при розрахунку boost балів: {e}")
            return 0.0
