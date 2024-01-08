from enum import Enum


class ItemType(Enum):
    PRODUCT = "PRODUCT"
    SERVICE = "SERVICE"


class ProductCategory(Enum):
    PRODUCTS = "PRODUCTS"
    TECHNIQUE = "TECHNIQUE"
    MEDICAL_DRUGS = "MEDICAL_DRUGS"
    HOUSEHOLD_CHEMICALS = "HOUSEHOLD CHEMICALS"


class ServiceCategory(Enum):
    TAXI = "TAXI"
    HAIRCUT = "HAIRCUT"
    MEDICAL_CHECKUP = "MEDICAL CHECKUP"
