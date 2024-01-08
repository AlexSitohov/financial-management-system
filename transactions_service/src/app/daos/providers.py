from app.daos.transactions_dao import TransactionsDAO
from motor.motor_asyncio import AsyncIOMotorClient


def provide_transactions_dao(mongo_client: AsyncIOMotorClient) -> TransactionsDAO:
    return TransactionsDAO(mongo_client)
