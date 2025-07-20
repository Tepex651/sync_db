from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.db.models.category import Category
    from app.db.models.image import Image
    from app.db.models.mark import Mark
    from app.db.models.parameter import Parameter

from app.db.models.associations import (product_category, product_mark,
                                        product_parameter)
from app.db.models.base import BaseModelDB


class Product(BaseModelDB):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    on_main: Mapped[bool] = mapped_column(Boolean, nullable=False)
    colors: Mapped[list[str]] = mapped_column(JSONB)
    excluded: Mapped[list[str]] = mapped_column(JSONB)
    extras: Mapped[list[str]] = mapped_column(JSONB)

    importance_num: Mapped[int | None] = mapped_column(Integer, nullable=True)

    moysklad_connector_products_data: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # one to many
    images: Mapped[list["Image"]] = relationship(
        "Image", back_populates="product", cascade="all, delete-orphan"
    )

    # many to many
    parameters: Mapped[list["Parameter"]] = relationship(
        "Parameter", secondary=product_parameter, back_populates="products"
    )
    marks: Mapped[list["Mark"]] = relationship(
        "Mark", secondary=product_mark, back_populates="products"
    )
    categories: Mapped[list["Category"]] = relationship(
        "Category", secondary=product_category, back_populates="products"
    )
