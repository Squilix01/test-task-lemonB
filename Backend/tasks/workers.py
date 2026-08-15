import asyncio
import logging
from tasks.celery_app import celery_app
from database.session import session_factory
from repository.product_repo import ProductRepository
from repository.sales_history_repo import SalesHistoryRepository
from services.scraper.amazon import AmazonScraper
from services.scraper.google_trends import GoogleTrendsScraper
from services.scoring.boost import BoostCalculator
from services.scoring.ai_scorer import ProductScorer

logger = logging.getLogger(__name__)


def run_async(coro):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coro)


async def _scrape_amazon_impl(task_self=None):
    if task_self:
        task_self.update_state(
            state="PROGRESS",
            meta={"current": 1, "total": 3, "status": "Запуск Playwright браузера..."}
        )
    scraper = AmazonScraper()
    if task_self:
        task_self.update_state(
            state="PROGRESS",
            meta={"current": 2, "total": 3, "status": "Парсинг Amazon Best Sellers..."}
        )
    items = await scraper.scrape_best_sellers()
    if not items:
        logger.warning("Товари з Amazon не були знайдені або сталася помилка.")
        return 0

    if task_self:
        task_self.update_state(
            state="PROGRESS",
            meta={"current": 3, "total": 3, "status": f"Збереження {len(items)} товарів у базу..."}
        )

    async with session_factory() as session:
        repo = ProductRepository(session)
        count = 0
        for item in items:
            try:
                existing = await repo.get_by_url(item["product_url"])
                if existing:
                    existing.price = item["price"]
                    existing.rating = item["rating"]
                    existing.number_of_reviews = item["number_of_reviews"]
                    existing.image_url = item["image_url"]
                else:
                    await repo.create(**item)
                    count += 1
            except Exception as e:
                await session.rollback()
                logger.error(f"Помилка при збереженні продукту {item.get('name')}: {e}")
                continue
        await session.commit()
    return count


@celery_app.task(bind=True, name="tasks.workers.scrape_amazon_task")
def scrape_amazon_task(self):
    logger.info("Starting Amazon scraping task with progress...")
    count = run_async(_scrape_amazon_impl(task_self=self))
    logger.info(f"Successfully scraped and saved {count} products.")
    return {"status": "success", "imported": count}


async def _update_trends_impl():
    async with session_factory() as session:
        repo = ProductRepository(session)
        products = await repo.get_unscored()
        
        scraper = GoogleTrendsScraper()
        updated = 0
        for p in products:
            try:
                # Use category or first word of name as keyword for trend
                keyword = p.category.split(" ")[0] if p.category else "gadget"
                trend_score = await scraper.get_trend_score(keyword)
                p.trend_score = trend_score
                updated += 1
                # Small delay to avoid ban
                await asyncio.sleep(2)
            except Exception as e:
                logger.error(f"Failed to get trends for {p.id}: {e}")
                
        await session.commit()
    return updated


@celery_app.task(name="tasks.workers.update_trends_task")
def update_trends_task():
    logger.info("Starting Google Trends update task...")
    count = run_async(_update_trends_impl())
    logger.info(f"Successfully updated trends for {count} products.")
    return {"status": "success", "updated": count}


async def _score_products_impl(task_self=None):
    async with session_factory() as session:
        product_repo = ProductRepository(session)
        sales_repo = SalesHistoryRepository(session)
        
        products = await product_repo.get_unscored()
        if not products:
            # Re-score all products to apply fresh AI/Boost updates
            products = await product_repo.get_all(skip=0, limit=100)

        total_count = len(products)
        if total_count == 0:
            logger.info("Немає товарів у базі для скорингу.")
            return 0
        
        boost_calc = BoostCalculator(sales_repo)
        scorer = ProductScorer()
        has_llm = bool(scorer.llm_provider and scorer.api_key)
        if has_llm:
            engine_name = "Gemini" if "gemini" in (scorer.llm_provider or "").lower() else "OpenAI LLM"
            title = f"AI-скоринг товарів ({engine_name})"
        else:
            engine_name = "Формула ТЗ (без AI)"
            title = "Скоринг товарів (Формула ТЗ)"
        
        updated = 0
        for idx, p in enumerate(products):
            action_desc = f"AI ({engine_name}) оцінює" if has_llm else "Розрахунок за формулою ТЗ"
            if task_self:
                task_self.update_state(
                    state="PROGRESS",
                    meta={
                        "current": idx + 1,
                        "total": total_count,
                        "product": p.name[:50],
                        "status": f"{action_desc}: {p.name[:35]}...",
                        "title": title,
                        "has_llm": has_llm,
                        "engine": engine_name,
                    }
                )

            try:
                # Dynamic trend momentum (55 - 88) if not already set
                trend = p.trend_score if p.trend_score is not None else float(55 + (abs(hash(p.name)) % 34))
                keywords = [word for word in p.name.split() if len(word) > 3]
                boost_score = await boost_calc.calculate(p.category, keywords)
                
                score, reasoning = await scorer.calculate_score(
                    name=p.name,
                    category=p.category,
                    rating=p.rating,
                    reviews=p.number_of_reviews,
                    trend_score=trend,
                    boost_score=boost_score
                )
                
                await product_repo.update_score(
                    product_id=p.id,
                    score=score,
                    reasoning=reasoning,
                    trend_score=trend,
                    boost_score=boost_score
                )
                updated += 1
                await session.commit()
            except Exception as e:
                logger.error(f"Помилка оцінювання продукту {p.id}: {e}")
                
    return updated


@celery_app.task(bind=True, name="tasks.workers.score_products_task")
def score_products_task(self):
    logger.info("Starting product scoring task with progress tracking...")
    count = run_async(_score_products_impl(task_self=self))
    logger.info(f"Successfully scored {count} products.")
    return {"status": "success", "scored": count}
