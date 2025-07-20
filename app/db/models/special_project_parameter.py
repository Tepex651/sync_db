from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModelDB


class SpecialProjectParameter(BaseModelDB):
    __tablename__ = "special_project_parameters"

    id: Mapped[int] = mapped_column(primary_key=True, default=1)

    parameters: Mapped[dict] = mapped_column(JSONB, nullable=True)
    actions: Mapped[list] = mapped_column(JSONB, nullable=True)
    badges: Mapped[list] = mapped_column(JSONB, nullable=True)
    json_parameters: Mapped[dict] = mapped_column(JSONB, nullable=True)
