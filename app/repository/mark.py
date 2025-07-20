from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.containers.mark import MarkIn
from app.containers.product import ProductIn
from app.db.models.associations import product_mark
from app.db.models.mark import Mark
from app.repository.base import BaseRepository


class MarkRepository(BaseRepository):
    model = Mark

    async def upsert(self, session: AsyncSession, marks: list[MarkIn]):
        marks_dicts = [mark.model_dump() for mark in marks]

        stmt = insert(self.model).values(marks_dicts)
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_=dict(
                name=stmt.excluded.name,
            ),
        )

        await session.execute(stmt)

    async def sync_product_marks(
        self, session: AsyncSession, products: list[ProductIn]
    ):
        products_marks_map = {
            product.id: {mark.id for mark in product.marks if mark.id is not None}
            for product in products
        }
        # delete old links
        for product_id, new_mark_ids in products_marks_map.items():
            await session.execute(
                delete(product_mark)
                .where(product_mark.c.product_id == product_id)
                .where(product_mark.c.mark_id.not_in(new_mark_ids))
            )

        # create new links
        all_links = []
        for product_id, new_mark_ids in products_marks_map.items():
            all_links.extend(
                [
                    {"product_id": product_id, "mark_id": mark_id}
                    for mark_id in new_mark_ids
                ]
            )

        if all_links:
            stmt = insert(product_mark).values(all_links).on_conflict_do_nothing()
            await session.execute(stmt)
