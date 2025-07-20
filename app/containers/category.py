from pydantic import BaseModel, Field


class CategoryIn(BaseModel):
    __tablename__ = "categories"

    id: int = Field(alias="Category_ID")
    name: str = Field(alias="Category_Name")
    image: str | None = Field(alias="Category_Image")
    sort_order: int
