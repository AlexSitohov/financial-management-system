from fastapi import APIRouter, Depends

from app.models.users_model import UsersModel
from app.repositories.providers import provide_users_repository_stub
from app.repositories.users_repository import UsersRepository

users_router = APIRouter(tags=["users"], prefix="/users/api/v1")


@users_router.post("/user", status_code=201, response_model=UsersModel.GET)
async def create_one(
        user_dto: UsersModel.CREATE,
        users_repository: UsersRepository = Depends(provide_users_repository_stub),
):
    return await users_repository.create_one(user_dto)


@users_router.get("/users", response_model=list[UsersModel.GET])
async def find_all(
        limit: int = 10,
        users_repository: UsersRepository = Depends(provide_users_repository_stub),
):
    return await users_repository.find_all(limit)


@users_router.delete("/user/{user_id}", status_code=204)
async def delete_one(
        user_id: str,
        users_repository: UsersRepository = Depends(provide_users_repository_stub),
):
    await users_repository.delete_one(user_id)


@users_router.get("/user/{user_id}", response_model=UsersModel.GET | None)
async def find_one(
        user_id: str,
        users_repository: UsersRepository = Depends(provide_users_repository_stub),
):
    return await users_repository.find_one(user_id)


@users_router.post("/login", status_code=200)
async def login(
        user_dto: UsersModel.LOGIN,
        users_repository: UsersRepository = Depends(provide_users_repository_stub),
):
    return await users_repository.login(user_dto)

