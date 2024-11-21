import uuid
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.core.config import settings
import os

rest_router = APIRouter()

@rest_router.get("/")
async def index():
    return {
        "message": "Hello World"
    }

@rest_router.get("/image")
async def media_image(image_id: uuid.UUID):
    if not image_id:
        raise HTTPException(status_code=400, detail="Invalid image ID")
    image_path = os.path.join(settings.PATHS.MEDIA_DIR, "images", f"{image_id}.jpg")
    if os.path.exists(image_path):
        return FileResponse(image_path)
    else:
        raise HTTPException(status_code=404, detail="Image not found")