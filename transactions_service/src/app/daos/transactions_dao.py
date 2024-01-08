from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import mongo_db_name, mongo_collection_name

from app.dblayer.enums import ItemsCategory


class TransactionsDAO:
    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.mongo_client = mongo_client
        self.database = mongo_client.get_database(mongo_db_name)
        self.collection = self.database.get_collection(mongo_collection_name)

    async def find_all(self, user_id: ObjectId, limit: int, skip: int):
        return (
            self.collection.find(
                filter=(
                    {
                        "$and": [
                            {"user_id": user_id},
                            {"deleted": {"$ne": True}},
                        ]
                    }
                )
            )
            .limit(limit)
            .skip(skip)
        )

    async def category_pipline_filter(
        self, user_id: ObjectId, category: ItemsCategory, limit: int, skip: int
    ):
        pipeline = [
            {
                "$match": {
                    "user_id": user_id,
                    "deleted": {"$ne": True},
                    "items.category": category,
                }
            },
            {"$unwind": "$items"},
            {"$match": {"items.category": category}},
            {
                "$group": {
                    "_id": "$_id",
                    "transaction_date": {"$first": "$transaction_date"},
                    "items": {"$push": "$items"},
                    "user_id": {"$first": "$user_id"},
                }
            },
            {"$skip": skip},
            {"$limit": limit},
        ]
        return await self.collection.aggregate(pipeline).to_list(length=None)
