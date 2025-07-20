from typing import ClassVar, Type

from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.containers.category import CategoryIn
from app.containers.product import ProductIn
from app.db.models.associations import product_category
from app.db.models.category import Category

from .base import BaseRepository


class CategoryRepository(BaseRepository):
    model: ClassVar[Type[Category]] = Category

    async def upsert(self, session: AsyncSession, categories: list[CategoryIn]):
        categories_dicts = [category.model_dump() for category in categories]

        stmt = insert(self.model).values(categories_dicts)
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_=dict(
                name=stmt.excluded.name,
                image=stmt.excluded.image,
                sort_order=stmt.excluded.sort_order,
            ),
        )

        await session.execute(stmt)

    async def sync_product_categories(
        self, session: AsyncSession, products: list[ProductIn]
    ):
        products_categories_map = {
            product.id: {category.id for category in product.categories}
            for product in products
        }
        # delete old links
        for product_id, new_category_ids in products_categories_map.items():
            await session.execute(
                delete(product_category)
                .where(product_category.c.product_id == product_id)
                .where(product_category.c.category_id.not_in(new_category_ids))
            )

        # create new links
        all_links = []
        for product_id, new_category_ids in products_categories_map.items():
            all_links.extend(
                [
                    {"product_id": product_id, "category_id": category_id}
                    for category_id in new_category_ids
                ]
            )

        if all_links:
            stmt = insert(product_category).values(all_links).on_conflict_do_nothing()
            await session.execute(stmt)
