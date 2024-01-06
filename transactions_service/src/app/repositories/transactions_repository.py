from fastapi import Request

from app.core.config import mongo_db_name, mongo_collection_name

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.new_types import StringToObjectId
from app.dblayer.serializer import mongo_serializer


class TransactionsRepository:
    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.mongo_client = mongo_client
        self.database = mongo_client.get_database(mongo_db_name)
        self.collection = self.database.get_collection(mongo_collection_name)

    @mongo_serializer
    async def create_one(self, transactions_dto: Request, user_id: StringToObjectId):
        (await transactions_dto.json())["user_id"] = user_id
        async with await self.mongo_client.start_session() as session:
            inserted_id = (
                await self.collection.insert_one(
                    document=await transactions_dto.json(), session=session
                )
            ).inserted_id
            return await self.collection.find_one(
                filter={"_id": inserted_id}, session=session
            )

    @mongo_serializer
    async def find_all(self, user_id: StringToObjectId, limit: int):
        return self.collection.find(
            filter={"$and": [{"user_id": user_id}, {"deleted": {"$ne": True}}]}
        ).limit(limit)

    @mongo_serializer
    async def delete_one(self, oid: StringToObjectId):
        await self.collection.update_one(
            filter={"_id": oid},
            update={"$set": {"deleted": True}},
        )

    @mongo_serializer
    async def find_one(self, oid: StringToObjectId):
        return await self.collection.find_one(
            filter={"_id": oid, "deleted": {"$ne": True}}
        )
