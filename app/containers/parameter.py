from pydantic import BaseModel, Field


class ParameterIn(BaseModel):
    id: int = Field(alias="Parameter_ID")
    name: str | None
    sort_order: int
    chosen: bool | None = None
    disabled: bool | None = None
    extra_field_color: str | None = None
    extra_field_image: str | None = None
    old_price: int | None = None
    parameter_string: str | None = None
    price: int
