from datetime import datetime

from bson import ObjectId
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
        id: ObjectId = Field(..., alias="_id")
        user_id: ObjectId
        items: ItemModel.GET | list[ItemModel.GET]
        total_amount: float | None = None
        count: int | None = None

        class Config:
            arbitrary_types_allowed = True
            json_encoders = {
                ObjectId: lambda x: str(x),
            }
