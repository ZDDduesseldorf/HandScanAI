import motor.motor_asyncio
from beanie import init_beanie

from app.core.config import settings
from app.db.models import MetadataModel, ImagesModel


async def init_db() -> None:
    """ Initialize the database and create the necessary models """

    client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)
    await init_beanie(database=client.db_name, document_models=[MetadataModel, ImagesModel])


    
