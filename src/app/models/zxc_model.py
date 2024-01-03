from typing import Optional

from pydantic import BaseModel, Field


class ItemModel:
    class Base(BaseModel):
        name: str
        description: Optional[str] = None
        price: float

        class Config:
            from_attribute = True

    class GET(Base):
        id: str = Field(alias="_id")

    class CREATE(Base):
        ...
