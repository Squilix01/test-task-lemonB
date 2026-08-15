from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_db, get_current_user
from repository.product_repo import ProductRepository
from schemas.product import ProductListResponse
from models.user import User
from tasks.workers import scrape_amazon_task, score_products_task


router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("", response_model=ProductListResponse)
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    repo = ProductRepository(session)
    products = await repo.get_all(skip=skip, limit=limit)
    total = await repo.get_count()
    return ProductListResponse(products=products, total=total)


@router.post("/scrape")
async def start_scrape(_: User = Depends(get_current_user)):
    task = scrape_amazon_task.delay()
    return {"task_id": task.id, "status": "started"}


@router.post("/score")
async def start_scoring(_: User = Depends(get_current_user)):
    task = score_products_task.delay()
    return {"task_id": task.id, "status": "started"}


@router.get("/tasks/{task_id}")
async def get_task_status(task_id: str, _: User = Depends(get_current_user)):
    from tasks.celery_app import celery_app
    from celery.result import AsyncResult

    res = AsyncResult(task_id, app=celery_app)
    state = res.state

    if state == "PENDING":
        return {
            "state": state,
            "current": 0,
            "total": 100,
            "status": "Ініціалізація та очікування в черзі Celery...",
            "product": "",
            "title": "",
            "engine": "",
            "has_llm": None,
        }
    elif state == "PROGRESS":
        info = res.info if isinstance(res.info, dict) else {}
        return {
            "state": state,
            "current": info.get("current", 0),
            "total": info.get("total", 100),
            "status": info.get("status", "Обробка..."),
            "product": info.get("product", ""),
            "title": info.get("title", ""),
            "engine": info.get("engine", ""),
            "has_llm": info.get("has_llm", None),
        }
    elif state == "SUCCESS":
        return {
            "state": state,
            "current": 100,
            "total": 100,
            "status": "Завершено успішно!",
            "result": res.result,
        }
    else:
        return {
            "state": state,
            "current": 0,
            "total": 100,
            "status": str(res.info) if res.info else "Помилка виконання задачі",
        }
