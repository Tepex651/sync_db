from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field

from .category import CategoryIn
from .image import ImageIn
from .mark import MarkIn
from .parameter import ParameterIn


def parse_rfc1123(value: str | None) -> datetime | None:
    if value is None:
        return
    try:
        return datetime.strptime(value, "%a, %d %b %Y %H:%M:%S %Z")
    except Exception as e:
        raise ValueError(f"Invalid RFC1123 date: {value}") from e


Rfc1123Date = Annotated[datetime, BeforeValidator(parse_rfc1123)]


class ProductIn(BaseModel):
    id: int = Field(alias="Product_ID")
    name: str = Field(alias="Product_Name")

    on_main: bool = Field(alias="OnMain")
    colors: list[dict]
    excluded: list[dict]
    extras: list[str]

    importance_num: int | None

    moysklad_connector_products_data: str | None

    created_at: Rfc1123Date = Field(alias="Created_At")
    updated_at: Rfc1123Date | None = Field(alias="Updated_At")

    # one to many
    images: list[ImageIn]
    parameters: list[ParameterIn]

    # many to many
    marks: list[MarkIn]
    categories: list[CategoryIn]

    class Config:
        validate_by_name = True
        extra = "ignore"
