from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from models.sales_history import SalesHistory


class SalesHistoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, skip: int = 0, limit: int = 50) -> list[SalesHistory]:
        result = await self.session.execute(
            select(SalesHistory)
            .order_by(SalesHistory.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_count(self) -> int:
        result = await self.session.execute(select(func.count(SalesHistory.id)))
        return result.scalar_one()

    async def create(self, **kwargs) -> SalesHistory:
        item = SalesHistory(**kwargs)
        self.session.add(item)
        await self.session.flush()
        return item

    async def bulk_create(self, items_data: list[dict]) -> list[SalesHistory]:
        items = [SalesHistory(**data) for data in items_data]
        self.session.add_all(items)
        await self.session.flush()
        return items

    async def delete(self, item_id: int) -> bool:
        item = await self.session.get(SalesHistory, item_id)
        if not item:
            return False
        await self.session.delete(item)
        await self.session.flush()
        return True

    async def search_by_category_or_keywords(
        self, category: str, keywords: list[str]
    ) -> list[SalesHistory]:
        conditions = [SalesHistory.category.ilike(f"%{category}%")]
        for kw in keywords:
            conditions.append(SalesHistory.keywords.ilike(f"%{kw}%"))
        result = await self.session.execute(
            select(SalesHistory).where(or_(*conditions))
        )
        return list(result.scalars().all())
