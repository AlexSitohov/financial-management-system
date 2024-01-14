from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field


class UsersModel:
    class Base(BaseModel):
        first_name: str
        last_name: str
        email: str
        password: str
        birthday_date: datetime | None = None
        salary: float | None = None
        spending_limit: float | None = None

        class Config:
            from_attribute = True

    class GET(Base):
        id: ObjectId = Field(alias="_id")

        class Config:
            arbitrary_types_allowed = True
            json_encoders = {
                ObjectId: lambda x: str(x),
            }

    class CREATE(Base):
        ...

    class LOGIN(BaseModel):
        email: str
        password: str

    class GETUserAfterLogin(BaseModel):
        email: str
        password: str
        id: ObjectId = Field(alias="_id")

        class Config:
            arbitrary_types_allowed = True
            json_encoders = {
                ObjectId: lambda x: str(x),
            }
