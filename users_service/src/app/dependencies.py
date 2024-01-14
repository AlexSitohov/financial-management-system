from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, Header, Path


async def validate_object_id(user_id: str = Path(...)) -> ObjectId:
    try:
        return ObjectId(user_id)
    except (TypeError, InvalidId):
        raise HTTPException(status_code=400, detail="Неверный формат ObjectId.")


async def get_object_id_from_header(user_id: str = Header(...)) -> ObjectId:
    return await validate_object_id(user_id)
