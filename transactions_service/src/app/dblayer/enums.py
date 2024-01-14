from enum import Enum


class ItemType(Enum):
    PRODUCT = "PRODUCT"
    SERVICE = "SERVICE"


class ProductCategory(Enum):
    PRODUCTS = "PRODUCTS"
    TECHNIQUE = "TECHNIQUE"
    MEDICAL_DRUGS = "MEDICAL_DRUGS"
    HOUSEHOLD_CHEMICALS = "HOUSEHOLD_CHEMICALS"


class ServiceCategory(Enum):
    TAXI = "TAXI"
    HAIRCUT = "HAIRCUT"
    MEDICAL_CHECKUP = "MEDICAL_CHECKUP"


ItemsCategory = Enum(
    "ItemsCategory", {**ProductCategory.__members__, **ServiceCategory.__members__}
)
