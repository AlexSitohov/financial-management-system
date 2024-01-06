from fastapi import APIRouter, Depends, Request, Header

from app.core.new_types import StringToObjectId
from app.repositories.providers import provide_transactions_repository_stub
from app.repositories.transactions_repository import TransactionsRepository

transactions_router = APIRouter(tags=["Transactions"], prefix="/transactions/api/v1")


@transactions_router.post("/transaction", status_code=201)
async def create_one(
    transaction_dto: Request,
    user_id: StringToObjectId = Header(),
    transactions_repository: TransactionsRepository = Depends(
        provide_transactions_repository_stub
    ),
):
    return await transactions_repository.create_one(transaction_dto, user_id)


@transactions_router.get("/transactions")
async def find_all(
    user_id: StringToObjectId = Header(),
    limit: int = 10,
    transactions_repository: TransactionsRepository = Depends(
        provide_transactions_repository_stub
    ),
):
    return await transactions_repository.find_all(user_id=user_id, limit=limit)


@transactions_router.delete("/transaction/{transaction_id}", status_code=204)
async def delete_one(
    transaction_id: StringToObjectId,
    transactions_repository: TransactionsRepository = Depends(
        provide_transactions_repository_stub
    ),
):
    await transactions_repository.delete_one(transaction_id)


@transactions_router.get("/transaction/{transaction_id}")
async def find_one(
    transaction_id: StringToObjectId,
    transactions_repository: TransactionsRepository = Depends(
        provide_transactions_repository_stub
    ),
):
    return await transactions_repository.find_one(transaction_id)
