from datetime import datetime
from typing import Union

from pydantic import BaseModel, Field, conlist

from app.models.item_model import ItemModel


class TransactionModel:
    class Base(BaseModel):
        transaction_date: datetime

        class Config:
            from_attributes = True

    class CREATE(Base):
        items: ItemModel.CREATE | conlist(ItemModel.CREATE, max_length=20)

    class GET(Base):
        id: str = Field(alias="_id")
        items: ItemModel.GET | list[ItemModel.GET]
