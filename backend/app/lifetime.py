from app.db.config import init_db


async def startup() -> None:
    await init_db()
