import logging
import os
from dataclasses import dataclass


@dataclass
class MongoConfig:
    mongo_db_login: str
    mongo_db_password: str
    mongo_db_host: str
    mongo_db_port: str
    mongo_db_name: str


db_config = MongoConfig(
    mongo_db_login=os.environ["ME_CONFIG_MONGODB_ADMINUSERNAME"],
    mongo_db_password=os.environ["ME_CONFIG_MONGODB_ADMINPASSWORD"],
    mongo_db_host=os.environ["MONGO_HOST"],
    mongo_db_port=os.environ["MONGO_PORT"],
    mongo_db_name=os.environ["MONGO_DB_NAME"],
)

mongo_db_name = os.environ["MONGO_DB_NAME"]
mongo_collection_name = os.environ["MONGO_COLLECTION_NAME"]


def configure_logging():
    FORMAT = "%(levelname)s %(asctime)s %(filename)s:%(lineno)d %(message)s"
    LEVEL = int(os.environ["LOGGING_LEVEL"])
    logging.basicConfig(level=LEVEL, format=FORMAT)
