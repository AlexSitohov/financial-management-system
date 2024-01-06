from functools import wraps
from bson.json_util import _json_convert

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCursor


async def _serialize_dict(document: dict):
    # return {
    #     field: str(document[field])
    #     if ObjectId.is_valid(document[field])
    #     else document[field]
    #     for field in document
    # }
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
