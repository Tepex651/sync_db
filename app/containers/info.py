from pydantic import BaseModel


class InfoOut(BaseModel):
    products_count: int
    categories_count: int
    marks_count: int
