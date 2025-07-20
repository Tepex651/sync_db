from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import BaseModelDB
from app.db.models.product import Product

from .associations import product_category


class Category(BaseModelDB):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    image: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    products: Mapped[list[Product]] = relationship(
        "Product", secondary=product_category, back_populates="categories"
    )
