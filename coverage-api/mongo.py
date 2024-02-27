import json
import logging

from async_lru import alru_cache
from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger()

MONGO_URI = "mongodb://mongo_db:27017/"


async def write_to_mongo(record: dict):
    try:
        logger.info("Writing to mongo: %s", record)
        mongo_client = await get_mongo_client()
        jsonified_dict = json.loads(json.dumps(record, default=str))
        await mongo_client["nirvana"].coverage.insert_one(jsonified_dict)
    except Exception:
        logger.exception("Error writing to mongo db")


@alru_cache
async def get_mongo_client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient(host=MONGO_URI)
