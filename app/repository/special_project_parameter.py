from typing import ClassVar, Type

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.special_project_parameter import SpecialProjectParameter
from app.repository.base import BaseRepository


class ProjectParameterRepository(BaseRepository):
    model: ClassVar[Type[SpecialProjectParameter]] = SpecialProjectParameter

    async def upsert(
        self,
        session: AsyncSession,
        parameters: dict,
        actions: list,
        badges: list,
        json_parameters: dict,
    ):

        stmt = insert(self.model).values(
            {
                "id": 1,
                "parameters": parameters,
                "actions": actions,
                "badges": badges,
                "json_parameters": json_parameters,
            }
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_=dict(
                parameters=stmt.excluded.parameters,
                actions=stmt.excluded.actions,
                badges=stmt.excluded.badges,
                json_parameters=stmt.excluded.json_parameters,
            ),
        )

        await session.execute(stmt)
