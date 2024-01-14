from functools import wraps
from bson.json_util import _json_convert

from motor.motor_asyncio import AsyncIOMotorCursor


async def _serialize_dict(document: dict):
    return _json_convert(document)


async def _serialize_cursor(cursor: AsyncIOMotorCursor):
    return [await _serialize_dict(document) async for document in cursor]


async def _serialize_list(documents_list: list):
    return [await _serialize_dict(document) for document in documents_list]


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
            return await _serialize_cursor(result)
        elif isinstance(result, list):
            return await _serialize_list(result)

    return wrapper_serialize
