from bson import ObjectId
from fastapi import HTTPException

from app.core.config import mongo_db_name, mongo_collection_name

from motor.motor_asyncio import AsyncIOMotorClient

from app.dblayer.serializer import mongo_serializer

from app.core.hash import hash_password, verify_password
from app.models.users_model import UsersModel


class UsersRepository:
    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.mongo_client = mongo_client
        self.database = mongo_client.get_database(mongo_db_name)
        self.collection = self.database.get_collection(mongo_collection_name)

    @mongo_serializer
    async def create_one(self, user_dto: UsersModel.CREATE):
        async with await self.mongo_client.start_session() as session:
            user_dto.password = await hash_password(user_dto.password)
            inserted_id = (
                await self.collection.insert_one(
                    document=user_dto.dict(exclude_none=True), session=session
                )
            ).inserted_id
            return await self.collection.find_one(
                filter={"_id": inserted_id}, session=session
            )

    @mongo_serializer
    async def find_all(self, limit: int, skip: int):
        return (
            self.collection.find(filter={"deleted": {"$ne": True}})
            .limit(limit)
            .skip(skip)
        )

    @mongo_serializer
    async def delete_one(self, oid: ObjectId):
        await self.collection.update_one(
            filter={"_id": oid}, update={"$set": {"deleted": True}}
        )

    @mongo_serializer
    async def find_one(self, oid: ObjectId, **kwargs):
        return await self.collection.find_one(
            filter={"_id": oid, "deleted": {"$ne": True}}
        )

    @mongo_serializer
    async def login(self, user_dto: UsersModel.LOGIN, **kwargs):
        user = await self.collection.find_one(
            filter={"email": user_dto.email, "deleted": {"$ne": True}}
        )
        if not await verify_password(user_dto.password, user["password"]):
            raise HTTPException(status_code=400, detail="Неверный логин или пароль")
        return user
