from pydantic import BaseModel, Field


class ImageIn(BaseModel):

    id: int = Field(alias="Image_ID")
    image_url: str = Field(alias="Image_URL")
    main_image: bool = Field(alias="MainImage")
    product_id: int = Field(alias="Product_ID")
    position: str | None
    sort_order: int
    title: str | None
