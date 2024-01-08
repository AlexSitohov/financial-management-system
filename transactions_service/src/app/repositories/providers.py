from motor.motor_asyncio import AsyncIOMotorClient

from app.repositories.transactions_repository import TransactionsRepository

from app.daos.transactions_dao import TransactionsDAO


def provide_transactions_repository_stub():
    raise NotImplementedError


def provide_transactions_repository(
    mongo_client: AsyncIOMotorClient, transactions_dao: TransactionsDAO
) -> TransactionsRepository:
    return TransactionsRepository(mongo_client, transactions_dao)
