from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import BaseModelDB


class Image(BaseModelDB):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image_url: Mapped[str] = mapped_column(String, nullable=False)
    main_image: Mapped[bool] = mapped_column(Boolean)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    position: Mapped[str | None] = mapped_column(String, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer)
    title: Mapped[str | None] = mapped_column(String, nullable=True)

    product = relationship("Product", back_populates="images")
