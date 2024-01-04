from datetime import datetime

from pydantic import BaseModel, Field


class UsersModel:
    class LOGIN(BaseModel):
        email: str
        password: str

        class Config:
            from_attribute = True
