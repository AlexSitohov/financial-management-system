from bson import ObjectId
from fastapi import APIRouter, Depends, Query

from app.models.users_model import UsersModel
from app.repositories.providers import provide_users_repository_stub
from app.repositories.users_repository import UsersRepository

from app.dblayer.serializer import validate_object_id

users_router = APIRouter(tags=["users"], prefix="/users/api/v1")


@users_router.post("/registration", status_code=201)
async def register(
    user_dto: UsersModel.CREATE,
    users_repository: UsersRepository = Depends(provide_users_repository_stub),
):
    return await users_repository.register(user_dto)


@users_router.get("/users")
async def find_all(
    limit: int = Query(default=5, gt=0, lt=101),
    skip: int = 0,
    users_repository: UsersRepository = Depends(provide_users_repository_stub),
):
    return await users_repository.find_all(limit, skip)


@users_router.delete("/user/{user_id}", status_code=204)
async def delete_one(
    user_id: ObjectId = Depends(validate_object_id),
    users_repository: UsersRepository = Depends(provide_users_repository_stub),
):
    await users_repository.delete_one(user_id)


@users_router.get("/user/{user_id}")
async def find_one(
    user_id: ObjectId = Depends(validate_object_id),
    users_repository: UsersRepository = Depends(provide_users_repository_stub),
):
    return await users_repository.find_one(user_id)


@users_router.post("/login", status_code=200)
async def login(
    user_dto: UsersModel.LOGIN,
    users_repository: UsersRepository = Depends(provide_users_repository_stub),
):
    return await users_repository.login(user_dto)
