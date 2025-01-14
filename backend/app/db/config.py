import motor.motor_asyncio
from beanie import init_beanie

from app.core.config import settings
from app.db.models import ScanEntry

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)


async def init_db() -> None:
    """Initialize the database and create the necessary models"""

    await init_beanie(database=client.db_name, document_models=[ScanEntry])


async def close_db() -> None:
    """Close the database connection"""

    client.close()


async def flush_db() -> None:
    """Flush the database"""

    await client.drop_database(client.db_name)
