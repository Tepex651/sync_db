from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.associations import product_parameter
from app.db.models.base import BaseModelDB


class Parameter(BaseModelDB):
    __tablename__ = "parameters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str | None] = mapped_column(None, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    chosen: Mapped[bool | None] = mapped_column(nullable=True)
    disabled: Mapped[bool | None] = mapped_column(nullable=True)
    extra_field_color: Mapped[None | str] = mapped_column(None, nullable=True)
    extra_field_image: Mapped[None | str] = mapped_column(None, nullable=True)
    old_price: Mapped[None | int] = mapped_column(None, nullable=True)
    parameter_string: Mapped[None | str] = mapped_column(None, nullable=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    products = relationship(
        "Product", secondary=product_parameter, back_populates="parameters"
    )
