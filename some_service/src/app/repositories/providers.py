from motor.motor_asyncio import AsyncIOMotorClient

from app.repositories.zxc_repository import ZXCRepository


def provide_zxc_repository_stub():
    raise NotImplementedError


def provide_zxc_repository(mongo_client: AsyncIOMotorClient) -> ZXCRepository:
    return ZXCRepository(mongo_client)
