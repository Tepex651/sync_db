from typing import ClassVar, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.base import BaseModelDB

ModelType = TypeVar("ModelType", bound=BaseModelDB)
ContainerType = TypeVar("ContainerType", bound=BaseModel)


class BaseRepository:
    model: ClassVar[Type[ModelType]]

    async def get_count(self, session: AsyncSession) -> int:
        result = await session.execute(select(func.count()).select_from(self.model))
        return result.scalar_one()
