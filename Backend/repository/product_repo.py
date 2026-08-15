from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.product import Product


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, skip: int = 0, limit: int = 50, sort_by_score: bool = True) -> list[Product]:
        query = select(Product)

        if sort_by_score:
            query = query.order_by(Product.score.desc().nullslast())

        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        
        return list(result.scalars().all())

    async def get_count(self) -> int:
        result = await self.session.execute(select(func.count(Product.id)))
        return result.scalar_one()

    async def get_by_id(self, product_id: int) -> Product | None:
        result = await self.session.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalar_one_or_none()

    async def get_by_url(self, product_url: str) -> Product | None:
        result = await self.session.execute(
            select(Product).where(Product.product_url == product_url)
        )
        return result.scalar_one_or_none()

    async def create(self, **kwargs) -> Product:
        product = Product(**kwargs)
        self.session.add(product)
        await self.session.flush()
        return product

    async def bulk_create(self, products_data: list[dict]) -> list[Product]:
        products = [Product(**data) for data in products_data]
        self.session.add_all(products)
        await self.session.flush()
        return products

    async def update_score(
        self,
        product_id: int,
        score: int,
        reasoning: str,
        trend_score: float | None = None,
        boost_score: float | None = None,
    ) -> Product | None:
        product = await self.get_by_id(product_id)
        if not product:
            return None
        product.score = score
        product.reasoning = reasoning
        if trend_score is not None:
            product.trend_score = trend_score
        if boost_score is not None:
            product.boost_score = boost_score
        await self.session.flush()
        return product

    async def get_unscored(self) -> list[Product]:
        result = await self.session.execute(
            select(Product).where(Product.score.is_(None))
        )
        return list(result.scalars().all())
