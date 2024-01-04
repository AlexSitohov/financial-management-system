from functools import wraps

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCursor


async def _serialize_dict(a):
    return {i: str(a[i]) if i == "_id" else a[i] for i in a}


async def _serialize_list(cursor: AsyncIOMotorCursor):
    return [await _serialize_dict(a) async for a in cursor]


def mongo_serializer(func):
    """
    A MongoDB deSerializer.
    deSerialize bson objects to python dicts.
    Serialize string to bson ObjectId.
    В будущем переписать с использованием pydantic, для исключения лишней сериализации.
    """

    @wraps(func)
    async def wrapper_serialize(repo_instance, *args, **kwargs):
        async with await repo_instance.mongo_client.start_session() as session:
            if args and isinstance(args[0], str):
                args = (ObjectId(args[0]),) + args[1:]

            kwargs["session"] = kwargs.get("session", session)
            result = await func(repo_instance, *args, **kwargs)
            if isinstance(result, dict):
                return await _serialize_dict(result)
            elif isinstance(result, AsyncIOMotorCursor):
                return [await _serialize_dict(d) async for d in result]
            else:
                return None

    return wrapper_serialize
