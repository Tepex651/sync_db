from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.associations import product_mark
from app.db.models.base import BaseModelDB

if TYPE_CHECKING:
    from app.db.models.product import Product


class Mark(BaseModelDB):
    __tablename__ = "marks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    products: Mapped[list["Product"]] = relationship(
        "Product", secondary=product_mark, back_populates="marks"
    )
