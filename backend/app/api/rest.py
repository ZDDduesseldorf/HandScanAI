import os

from fastapi.responses import FileResponse
from app.core.config import settings

async def get_index():
    file = os.path.join(settings.PATHS.STATIC_DIR, "index.html")
    if not os.path.exists(file):
        return {"error": "File not found"}
    return FileResponse(file)