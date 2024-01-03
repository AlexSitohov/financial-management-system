from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import MongoConfig


def get_mongo_client(config: MongoConfig) -> AsyncIOMotorClient:
    uri = (
        f"mongodb://{config.mongo_db_login}:{config.mongo_db_password}"
        f"@{config.mongo_db_host}:{config.mongo_db_port}"
    )
    return AsyncIOMotorClient(uri)
