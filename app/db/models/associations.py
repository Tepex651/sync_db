from sqlalchemy import Column, ForeignKey, Table

from .base import BaseModelDB

product_mark = Table(
    "product_marks",
    BaseModelDB.metadata,
    Column(
        "product_id", ForeignKey("products.id", ondelete="CASCADE"), primary_key=True
    ),
    Column("mark_id", ForeignKey("marks.id", ondelete="CASCADE"), primary_key=True),
)

product_category = Table(
    "product_categories",
    BaseModelDB.metadata,
    Column(
        "product_id", ForeignKey("products.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "category_id", ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True
    ),
)

product_parameter = Table(
    "product_parameters",
    BaseModelDB.metadata,
    Column(
        "product_id", ForeignKey("products.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "parameter_id",
        ForeignKey("parameters.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
