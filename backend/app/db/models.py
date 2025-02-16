import os
from beanie import Delete, Document, Save, before_event, after_event
from pydantic import Field
from datetime import datetime, timezone
from typing import Optional
from app.core.config import settings
from utils.key_enums import PipelineAPIKeys
from pipelines.add_new_embeddings_pipeline import run_add_new_embeddings_pipeline
from utils.uuid_utils import generate_uuid


class ScanEntry(Document):
    """Scan Entry Model"""

    id: str = Field(default_factory=lambda: generate_uuid())
    real_age: Optional[int] = Field(default=None)
    real_gender: Optional[int] = Field(default=None)
    confirmed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def image_exists(self) -> bool:
        """Check if the associated image exists in the folder"""
        photo_path = os.path.join(settings.PATHS.MEDIA_DIR, "QueryImages", f"{self.id}.jpg")
        return os.path.exists(photo_path)

    class Settings:
        collection = "scan_entries"
        indexes = ["id"]
        validate_on_save = True

    @before_event(Delete)
    async def before_delete(self):
        """before delete action"""
        if self.confirmed:
            raise ValueError("ScanEntry is already confirmed and cannot be removed.")

        photo_path = os.path.join(settings.PATHS.MEDIA_DIR, "QueryImages", f"{self.id}.jpg")
        if os.path.exists(photo_path):
            os.remove(photo_path)

    @before_event(Save)
    async def before_save(self):
        """before saving action"""
        old_instance = await self.get(self.id)
        if old_instance and old_instance.confirmed:
            raise ValueError("Cannot modify a confirmed ScanEntry.")

        if self.real_age is not None and self.real_age < 0:
            raise ValueError("real age must be a positive number")

        if self.real_gender is not None and self.real_gender not in [0, 1]:
            raise ValueError("real gender must be either 0 (female) or 1 (male)")

        if self.confirmed and (not self.image_exists or self.real_age is None or self.real_gender is None):
            raise ValueError("Cannot confirm ScanEntry without an image, valid real_age or real_gender.")

    @after_event(Save)
    async def after_save(self):
        """after saving action"""

        if self.image_exists and self.confirmed and self.real_age is not None and self.real_gender is not None:
            ground_truth_data = {
                PipelineAPIKeys.REAL_AGE.value: self.real_age,
                PipelineAPIKeys.REAL_GENDER.value: self.real_gender,
            }

            run_add_new_embeddings_pipeline(self.id, ground_truth_data, testing=False)
