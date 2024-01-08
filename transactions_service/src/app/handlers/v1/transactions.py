from bson import ObjectId
from fastapi import APIRouter, Depends, Query
from app.repositories.providers import provide_transactions_repository_stub
from app.repositories.transactions_repository import TransactionsRepository

from app.dblayer.serializer import get_object_id_from_header, validate_object_id

from app.models.transaction_model import TransactionModel

transactions_router = APIRouter(tags=["Transactions"], prefix="/transactions/api/v1")


@transactions_router.post("/transaction", status_code=201)
async def create_one(
    transaction_dto: TransactionModel.CREATE,
    user_id: ObjectId = Depends(get_object_id_from_header),
    transactions_repository: TransactionsRepository = Depends(
        provide_transactions_repository_stub
    ),
):
    return await transactions_repository.create_one(transaction_dto, user_id)


@transactions_router.get("/transactions")
async def find_all(
    user_id: ObjectId = Depends(get_object_id_from_header),
    limit: int = Query(default=5, gt=0, lt=101),
    skip: int = 0,
    transactions_repository: TransactionsRepository = Depends(
        provide_transactions_repository_stub
    ),
):
    return await transactions_repository.find_all(user_id, limit, skip)


@transactions_router.delete("/transaction/{transaction_id}", status_code=204)
async def delete_one(
    transaction_id: ObjectId = Depends(validate_object_id),
    user_id: ObjectId = Depends(get_object_id_from_header),
    transactions_repository: TransactionsRepository = Depends(
        provide_transactions_repository_stub
    ),
):
    await transactions_repository.delete_one(transaction_id, user_id)


@transactions_router.get("/transaction/{transaction_id}")
async def find_one(
    transaction_id: ObjectId = Depends(validate_object_id),
    user_id: ObjectId = Depends(get_object_id_from_header),
    transactions_repository: TransactionsRepository = Depends(
        provide_transactions_repository_stub
    ),
):
    return await transactions_repository.find_one(transaction_id, user_id)
