from datetime import datetime

from bson import ObjectId
from fastapi import APIRouter, Depends, Query
from app.repositories.providers import provide_transactions_repository_stub
from app.repositories.transactions_repository import TransactionsRepository

from app.dependencies import get_object_id_from_header, validate_object_id

from app.models.transaction_model import TransactionModel

from app.dblayer.enums import ItemsCategory

from app.dependencies import get_item_category

transactions_router = APIRouter(tags=["Transactions"], prefix="/transactions/api/v1")


@transactions_router.post("/transactions", status_code=201)
async def create_transaction(
    transaction_dto: TransactionModel.CREATE,
    user_id: ObjectId = Depends(get_object_id_from_header),
    transactions_repository: TransactionsRepository = Depends(
        provide_transactions_repository_stub
    ),
):
    return await transactions_repository.create_one(transaction_dto, user_id)


@transactions_router.get("/transactions")
async def find_transactions(
    user_id: ObjectId = Depends(get_object_id_from_header),
    category: ItemsCategory | None = Depends(get_item_category),
    limit: int = Query(default=5, gt=0, lt=101),
    skip: int = Query(default=0),
    transactions_repository: TransactionsRepository = Depends(
        provide_transactions_repository_stub
    ),
):
    return await transactions_repository.find_all(user_id, category, limit, skip)


@transactions_router.delete("/transactions/{transaction_id}", status_code=204)
async def delete_transaction(
    transaction_id: ObjectId = Depends(validate_object_id),
    user_id: ObjectId = Depends(get_object_id_from_header),
    transactions_repository: TransactionsRepository = Depends(
        provide_transactions_repository_stub
    ),
):
    await transactions_repository.delete_one(transaction_id, user_id)


@transactions_router.get("/transactions/{transaction_id}")
async def find_transaction(
    transaction_id: ObjectId = Depends(validate_object_id),
    user_id: ObjectId = Depends(get_object_id_from_header),
    transactions_repository: TransactionsRepository = Depends(
        provide_transactions_repository_stub
    ),
):
    return await transactions_repository.find_one(transaction_id, user_id)


@transactions_router.get("/transactions/statistic/calculate_expenses")
async def calculate_expenses(
    timestamp_start: datetime = Query(),
    timestamp_end: datetime = Query(),
    user_id: ObjectId = Depends(get_object_id_from_header),
    transactions_repository: TransactionsRepository = Depends(
        provide_transactions_repository_stub
    ),
):
    return await transactions_repository.calculate_expenses(
        timestamp_start, timestamp_end, user_id
    )
