from motor.motor_asyncio import AsyncIOMotorClient

from app.repositories.transactions_repository import TransactionsRepository


def provide_transactions_repository_stub():
    raise NotImplementedError


def provide_transactions_repository(
    mongo_client: AsyncIOMotorClient,
) -> TransactionsRepository:
    return TransactionsRepository(mongo_client)
