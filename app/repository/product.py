from typing import ClassVar, Type

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.containers.product import ProductIn
from app.db.models.product import Product
from app.repository.base import BaseRepository
from app.repository.category import CategoryRepository
from app.repository.image import ImageReposotory
from app.repository.mark import MarkRepository
from app.repository.parameter import ParameterReposotory


class ProductRepository(BaseRepository):
    model: ClassVar[Type[Product]] = Product

    def __init__(self):
        self.image_repo = ImageReposotory()
        self.params_repo = ParameterReposotory()
        self.mark_repo = MarkRepository()
        self.category_repo = CategoryRepository()
        self.batch_size = 100

    async def upsert(self, session: AsyncSession, products: list[ProductIn]):
        products_dicts = [
            product.model_dump(exclude={"images", "parameters", "marks", "categories"})
            for product in products
        ]

        stmt = insert(self.model).values(products_dicts)
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_=dict(
                name=stmt.excluded.name,
                on_main=stmt.excluded.on_main,
                colors=stmt.excluded.colors,
                excluded=stmt.excluded.excluded,
                extras=stmt.excluded.extras,
                importance_num=stmt.excluded.importance_num,
                moysklad_connector_products_data=stmt.excluded.moysklad_connector_products_data,
                created_at=stmt.excluded.created_at,
                updated_at=stmt.excluded.updated_at,
            ),
        )

        await session.execute(stmt)

        # update images
        images = [image for product in products for image in product.images]
        await self.image_repo.upsert(session=session, images=images)

        # update product params
        params = [param for product in products for param in product.parameters]
        await self.params_repo.upsert(session=session, parameters=params)
        await self.params_repo.sync_product_parameters(
            session=session, products=products
        )

        # update product mark links
        await self.mark_repo.sync_product_marks(session=session, products=products)

        # update category links
        await self.category_repo.sync_product_categories(
            session=session, products=products
        )
