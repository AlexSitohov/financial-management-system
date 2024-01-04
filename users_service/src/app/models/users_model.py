from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UsersModel:
    class Base(BaseModel):
        first_name: str
        last_name: str
        email: str
        birthday_date: datetime

        class Config:
            from_attribute = True

    class GET(Base):
        id: str = Field(alias="_id")

    class CREATE(Base):
        ...
