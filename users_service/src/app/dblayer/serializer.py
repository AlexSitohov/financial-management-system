from functools import wraps
from bson.json_util import (
    _json_convert,
    dumps,
    CANONICAL_JSON_OPTIONS,
    loads,
    LEGACY_JSON_OPTIONS,
    JSONOptions,
)

from bson import ObjectId, json_util
from motor.motor_asyncio import AsyncIOMotorCursor

from bson.errors import InvalidId
from fastapi import HTTPException, Header, Path


async def _serialize_dict(document: dict):
    return _json_convert(document)


async def _serialize_list(cursor: AsyncIOMotorCursor):
    return [await _serialize_dict(document) async for document in cursor]


def mongo_serializer(func):
    """
    A MongoDB deSerializer.
    deSerialize bson objects to python dicts.
    """

    @wraps(func)
    async def wrapper_serialize(*args, **kwargs):
        result = await func(*args, **kwargs)
        if isinstance(result, dict):
            return await _serialize_dict(result)
        elif isinstance(result, AsyncIOMotorCursor):
            return await _serialize_list(result)
        else:
            return None

    return wrapper_serialize


async def validate_object_id(user_id: str = Path(...)) -> ObjectId:
    try:
        return ObjectId(user_id)
    except (TypeError, InvalidId):
        raise HTTPException(status_code=400, detail="Неверный формат ObjectId.")


async def get_object_id_from_header(user_id: str = Header(...)) -> ObjectId:
    return await validate_object_id(user_id)
