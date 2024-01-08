from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, Header, Path

from app.dblayer.enums import ItemsCategory


async def get_item_category(category: str | None = None):
    if category:
        try:
            category_enum = ItemsCategory[category].value.value
            return category_enum
        except KeyError:
            valid_keys = ", ".join(ItemsCategory.__members__.keys())
            raise HTTPException(
                status_code=400, detail=f"Category must be one of: {valid_keys}"
            )
    return None


async def validate_object_id(transaction_id: str = Path(...)) -> ObjectId:
    try:
        return ObjectId(transaction_id)
    except (TypeError, InvalidId):
        raise HTTPException(status_code=400, detail="Неверный формат ObjectId.")


async def get_object_id_from_header(user_id: str = Header(...)) -> ObjectId:
    return await validate_object_id(user_id)
