from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime, timezone


class TestModel(Document):
    """ Test Model """

    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        collection = "test_model"
