from pydantic import BaseModel, Field


class MarkIn(BaseModel):
    id: int = Field(alias="Mark_ID")
    name: str = Field(alias="Mark_Name")
