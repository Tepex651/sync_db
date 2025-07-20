from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.containers.image import ImageIn
from app.db.models.image import Image
from app.repository.base import BaseRepository


class ImageReposotory(BaseRepository):
    model = Image

    async def delete_old_images(self, session: AsyncSession, images: list[ImageIn]):
        images_by_product: dict[int, list[ImageIn]] = {}
        for img in images:
            images_by_product.setdefault(img.product_id, []).append(img)

        for product_id, imgs in images_by_product.items():
            new_image_ids = {img.id for img in imgs}

            stmt = delete(self.model).where(self.model.product_id == product_id)
            if new_image_ids:
                stmt = stmt.where(self.model.id.notin_(new_image_ids))
            await session.execute(stmt)

    async def upsert(self, session: AsyncSession, images: list[ImageIn]):
        await self.delete_old_images(session=session, images=images)

        images_dicts = [image.model_dump() for image in images]

        stmt = insert(self.model).values(images_dicts)
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_=dict(
                image_url=stmt.excluded.image_url,
                main_image=stmt.excluded.main_image,
                product_id=stmt.excluded.product_id,
                position=stmt.excluded.position,
                sort_order=stmt.excluded.sort_order,
                title=stmt.excluded.title,
            ),
        )

        await session.execute(stmt)
