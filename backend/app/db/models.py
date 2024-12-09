from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime, timezone


class ValidatedData(Document):
    """ Validated Data """

    hand_side: str
    gender: Optional[str] = None
    age: int
    job_type: str

class CameraConfiguration(Document):
    """ Camera Configuration """

    camera_type: str
    camera_position: str
    resolution: tuple[int]


class MetadataModel(Document):
    """ MetadataModel """
    UUID: str
    person_id: int
    age: int
    gender: str
    skin_colour: str 
    accessories: int
    nail_polish: int
    aspect_of_hand: str
    eleven_k_hands_image_name: str
    irregularities: int

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    camera_configuration: CameraConfiguration
    validated_data: ValidatedData

    class Settings:
        collection = "Metadata_model"
        indexes = ("UUID", 1)

class HandRegionsModel(Document):
    """ Test Model """

    UUID: str
    region: str
    image: Optional[str] = None # TODO 

    class Settings:
        collection = "Hand_regions_model"
        indexes = [
            [("UUID", 1), ("region", 1)]
        ]

