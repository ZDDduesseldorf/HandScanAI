from app.db.config import init_db
from utils.logging_utils import setup_csv_logging


async def startup() -> None:
    """Startup event"""

    await init_db()
    setup_csv_logging()
