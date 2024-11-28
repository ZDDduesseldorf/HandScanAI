import motor.motor_asyncio
from beanie import init_beanie

from app.core.config import settings
from app.db.models import TestModel

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)


async def init_db() -> None:
    await init_beanie(database=client.db_name, document_models=[TestModel])
