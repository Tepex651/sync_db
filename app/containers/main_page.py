from pydantic import BaseModel, Field

from .category import CategoryIn
from .mark import MarkIn
from .product import ProductIn


class MainPageDataIn(BaseModel):
    products: list[ProductIn]
    categories: list[CategoryIn]
    marks: list[MarkIn] = Field(default_factory=list, alias="product_marks")

    project_parameters: dict = Field(alias="special_project_parameters")
    project_actions: list = Field(alias="special_project_parameters_actions")
    project_badges: list = Field(alias="special_project_parameters_badges")
    project_json_parameters: dict = Field(alias="special_project_parameters_json")
