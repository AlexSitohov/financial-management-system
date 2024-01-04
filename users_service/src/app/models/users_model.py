from datetime import datetime

from pydantic import BaseModel, Field


class UsersModel:
    class Base(BaseModel):
        first_name: str
        last_name: str
        email: str
        password: str
        birthday_date: datetime
        salary: str | None
        spending_limit: str | None

        class Config:
            from_attribute = True

    class GET(Base):
        id: str = Field(alias="_id")

    class CREATE(Base):
        ...

    class LOGIN(BaseModel):
        email: str
        password: str
