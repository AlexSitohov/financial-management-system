from pydantic import BaseModel, Field

from app.dblayer.enums import (
    ProductCategory,
    ItemType,
    ServiceCategory,
)


class ItemModel:
    class Base(BaseModel):
        item_name: str
        price: float
        item_type: ItemType
        category: ProductCategory | ServiceCategory

        qty: int | None = None
        weight: int | None = None
        milligram: int | None = None
        color: str | None = None

        class Config:
            from_attributes = True
            use_enum_values = True

    class CREATE(Base):
        ...

    class GET(Base):
        ...
