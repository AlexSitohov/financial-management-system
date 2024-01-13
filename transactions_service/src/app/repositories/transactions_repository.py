from datetime import datetime

from app.core.config import mongo_db_name, mongo_collection_name
from bson import ObjectId

from motor.motor_asyncio import AsyncIOMotorClient

from app.dblayer.serializer import mongo_serializer

from app.models.transaction_model import TransactionModel

from app.daos.transactions_dao import TransactionsDAO

from app.dblayer.enums import ItemsCategory


class TransactionsRepository:
    def __init__(
        self, mongo_client: AsyncIOMotorClient, transactions_dao: TransactionsDAO
    ):
        self.mongo_client = mongo_client
        self.transactions_dao = transactions_dao
        self.database = mongo_client.get_database(mongo_db_name)
        self.collection = self.database.get_collection(mongo_collection_name)

    @mongo_serializer
    async def create_one(
        self, transactions_dto: TransactionModel.CREATE, user_id: ObjectId
    ):
        transactions_dto = transactions_dto.dict(exclude_none=True)
        transactions_dto["user_id"] = user_id
        async with await self.mongo_client.start_session() as session:
            transaction_id = (
                await self.collection.insert_one(
                    document=transactions_dto, session=session
                )
            ).inserted_id
            return await self.collection.find_one(
                filter={"_id": transaction_id}, session=session
            )

    @mongo_serializer
    async def find_all(
        self, user_id: ObjectId, category: ItemsCategory | None, limit: int, skip: int
    ):
        if category:
            return await self.transactions_dao.category_pipline_filter(
                user_id, category, limit, skip
            )

        return await self.transactions_dao.find_all(user_id, limit, skip)

    @mongo_serializer
    async def delete_one(self, transaction_id: ObjectId, user_id: ObjectId):
        await self.collection.update_one(
            filter={
                "$and": [
                    {"_id": transaction_id},
                    {"user_id": user_id},
                    {"deleted": {"$ne": True}},
                ]
            },
            update={"$set": {"deleted": True}},
        )

    @mongo_serializer
    async def find_one(self, transaction_id: ObjectId, user_id: ObjectId):
        return await self.collection.find_one(
            filter={
                "$and": [
                    {"_id": transaction_id},
                    {"user_id": user_id},
                    {"deleted": {"$ne": True}},
                ]
            },
        )

    async def calculate_expenses(
        self, timestamp_start: datetime, timestamp_end: datetime, user_id: ObjectId
    ):
        return await self.transactions_dao.calculate_expenses(
            timestamp_start, timestamp_end, user_id
        )
