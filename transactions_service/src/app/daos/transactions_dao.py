from datetime import datetime

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import mongo_db_name, mongo_collection_name

from app.dblayer.enums import ItemsCategory


class TransactionsDAO:
    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.mongo_client = mongo_client
        self.database = mongo_client.get_database(mongo_db_name)
        self.collection = self.database.get_collection(mongo_collection_name)

    async def find_all(
        self,
        user_id: ObjectId,
        category: ItemsCategory | None,
        limit: int,
        skip: int,
    ):
        match_stage = {"user_id": user_id, "deleted": {"$ne": True}}

        if category:
            match_stage["items.category"] = category

        pipeline = [
            {"$match": match_stage},
            {"$unwind": "$items"},
            {"$match": {"items.category": category}} if category else {"$match": {}},
            {
                "$group": {
                    "_id": "$_id",
                    "transaction_date": {"$first": "$transaction_date"},
                    "items": {"$push": "$items"},
                    "total_amount": {
                        "$sum": {
                            "$multiply": [
                                "$items.price",
                                {"$ifNull": ["$items.qty", 1]},
                            ]
                        }
                    },
                    "count": {"$sum": 1},
                    "user_id": {"$first": "$user_id"},
                }
            },
            {"$sort": {"transaction_date": -1}},
            {"$skip": skip},
            {"$limit": limit},
        ]

        async with self.collection.aggregate(pipeline) as cursor:
            return await cursor.to_list(length=None)

    async def calculate_expenses(
        self, timestamp_start: datetime, timestamp_end: datetime, user_id: ObjectId
    ):
        pipeline = [
            {
                "$match": {
                    "user_id": user_id,
                    "deleted": {"$ne": True},
                    "transaction_date": {
                        "$gte": timestamp_start,
                        "$lt": timestamp_end,
                    },
                }
            },
            {"$unwind": "$items"},
            {
                "$group": {
                    "_id": {"category": "$items.category"},
                    "total_price": {
                        "$sum": {
                            "$multiply": [
                                "$items.price",
                                {"$ifNull": ["$items.qty", 1]},
                            ]
                        }
                    },
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_price": {"$sum": "$total_price"},
                    "categories": {
                        "$push": {
                            "category": "$_id.category",
                            "price": "$total_price",
                        }
                    },
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "total_price": 1,
                    "categories": 1,
                }
            },
        ]

        async with self.collection.aggregate(pipeline) as cursor:
            if result := await cursor.to_list(length=1):
                return result[0]
