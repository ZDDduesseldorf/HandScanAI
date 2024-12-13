import motor.motor_asyncio
from beanie import init_beanie

from app.core.config import settings
from app.db.models import MetadataModel, ImagesModel

from uuid import UUID

async def init_db() -> None:
    """ Initialize the database and create the necessary models """

    client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)
    await init_beanie(database=client.db_name, document_models=[MetadataModel, ImagesModel])

    await MetadataModel.get_motor_collection().drop()

    entry = MetadataModel(
        id= "0a767b07-147d-42f8-ae42-ab37e9bbe7f2", 
        age=10, 
        gender= "Female", 
        camera_configuration_id= 1)

    await entry.insert()

    result = await MetadataModel.find(MetadataModel.id == UUID("0a767b07-147d-42f8-ae42-ab37e9bbe7f2")).to_list()
    print(result)
    
