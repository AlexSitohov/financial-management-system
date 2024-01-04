from fastapi import APIRouter, Depends, Request

from app.models.zxc_model import ItemModel
from app.repositories.providers import provide_zxc_repository_stub
from app.repositories.zxc_repository import ZXCRepository

zxc_router = APIRouter(tags=["zxc"], prefix="/zxc/api/v1")


@zxc_router.post("/create_one", status_code=201, response_model=ItemModel.GET)
async def create_one(
    zxc_dto: ItemModel.CREATE,
    zxc_repository: ZXCRepository = Depends(provide_zxc_repository_stub),
):
    return await zxc_repository.create_one(zxc_dto)


@zxc_router.get("/find_all", response_model=list[ItemModel.GET])
async def find_all(
    limit: int = 10,
    zxc_repository: ZXCRepository = Depends(provide_zxc_repository_stub),
):
    return await zxc_repository.find_all(limit)


@zxc_router.delete("/delete_one/{id}", status_code=204)
async def delete_one(
    id: str,
    zxc_repository: ZXCRepository = Depends(provide_zxc_repository_stub),
):
    await zxc_repository.delete_one(id)


@zxc_router.get("/find_one/{id}", response_model=ItemModel.GET)
async def find_one(
    id: str,
    zxc_repository: ZXCRepository = Depends(provide_zxc_repository_stub),
):
    return await zxc_repository.find_one(id)
