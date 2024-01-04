from motor.motor_asyncio import AsyncIOMotorClient

from app.repositories.users_repository import UsersRepository


def provide_users_repository_stub():
    raise NotImplementedError


def provide_users_repository(mongo_client: AsyncIOMotorClient) -> UsersRepository:
    return UsersRepository(mongo_client)
