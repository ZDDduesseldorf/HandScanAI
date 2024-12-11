from app.db.config import init_db


async def startup() -> None:
    """ Startup event """

    await init_db()
