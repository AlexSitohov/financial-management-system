from datetime import datetime

from pydantic import BaseModel, Field


class UsersModel:
    class REGISTRATION(BaseModel):
        first_name: str
        last_name: str
        email: str
        password: str
        birthday_date: datetime | None = None
        salary: str | None = None
        spending_limit: str | None = None

        class Config:
            from_attribute = True

    class LOGIN(BaseModel):
        email: str
        password: str

        class Config:
            from_attribute = True
