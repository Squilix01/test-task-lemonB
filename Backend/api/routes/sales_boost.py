from fastapi import APIRouter, Depends, UploadFile, File, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_db, get_current_user
from repository.sales_history_repo import SalesHistoryRepository
from schemas.sales_history import (
    SalesHistoryCreate,
    SalesHistoryResponse,
    SalesHistoryListResponse,
)
from services.csv_import import parse_sales_csv
from models.user import User


router = APIRouter(prefix="/api/sales-boost", tags=["sales-boost"])


@router.get("", response_model=SalesHistoryListResponse)
async def get_sales_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    repo = SalesHistoryRepository(session)
    items = await repo.get_all(skip=skip, limit=limit)
    total = await repo.get_count()
    return SalesHistoryListResponse(items=items, total=total)


@router.post("", response_model=SalesHistoryResponse, status_code=status.HTTP_201_CREATED)
async def create_sales_history(
    data: SalesHistoryCreate,
    session: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    repo = SalesHistoryRepository(session)
    item = await repo.create(**data.model_dump())
    return item


@router.post("/csv", status_code=status.HTTP_201_CREATED)
async def upload_csv(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Файл повинен бути у форматі CSV.",
        )

    content = await file.read()
    items_data = parse_sales_csv(content.decode("utf-8"))

    repo = SalesHistoryRepository(session)
    items = await repo.bulk_create(items_data)
    return {"imported": len(items)}


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sales_history(
    item_id: int,
    session: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    repo = SalesHistoryRepository(session)
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запис не знайдено.",
        )
