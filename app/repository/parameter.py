from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.containers.parameter import ParameterIn
from app.containers.product import ProductIn
from app.db.models.associations import product_parameter
from app.db.models.parameter import Parameter
from app.repository.base import BaseRepository


class ParameterReposotory(BaseRepository):
    model = Parameter

    async def sync_product_parameters(
        self, session: AsyncSession, products: list[ProductIn]
    ):
        products_parameters_map = {
            product.id: {param.id for param in product.parameters}
            for product in products
        }
        # delete old links
        for product_id, new_parameter_ids in products_parameters_map.items():
            await session.execute(
                delete(product_parameter)
                .where(product_parameter.c.product_id == product_id)
                .where(product_parameter.c.parameter_id.not_in(new_parameter_ids))
            )

        # create new links
        all_links = []
        for product_id, new_parameter_ids in products_parameters_map.items():
            all_links.extend(
                [
                    {"product_id": product_id, "parameter_id": parameter_id}
                    for parameter_id in new_parameter_ids
                ]
            )

        if all_links:
            stmt = insert(product_parameter).values(all_links).on_conflict_do_nothing()
            await session.execute(stmt)

    async def upsert(self, session: AsyncSession, parameters: list[ParameterIn]):
        params_dicts = [param.model_dump() for param in parameters]

        stmt = insert(self.model).values(params_dicts)
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_=dict(
                name=stmt.excluded.name,
                sort_order=stmt.excluded.sort_order,
                chosen=stmt.excluded.chosen,
                disabled=stmt.excluded.disabled,
                extra_field_color=stmt.excluded.extra_field_color,
                extra_field_image=stmt.excluded.extra_field_image,
                old_price=stmt.excluded.old_price,
                parameter_string=stmt.excluded.parameter_string,
                price=stmt.excluded.price,
            ),
        )

        await session.execute(stmt)
