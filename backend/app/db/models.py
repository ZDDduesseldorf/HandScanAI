from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime, timezone
from uuid import UUID


class CameraConfiguration(Document):
    """ Camera Configuration """

    configuration_id : int
    camera_type: str
    camera_position: str
    height: int
    width: int


class MetadataModel(Document):
    """ MetadataModel """
    id: UUID
    age: int
    age_confirmed: bool = False 
    gender: str
    gender_confirmed: bool = False

    person_id: Optional[int]
    skin_colour: Optional[str]
    accessories: Optional[int] 
    nail_polish: Optional[int]
    aspect_of_hand: Optional[str]
    eleven_k_hands_image_name: Optional[str]
    irregularities: Optional[int]

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    camera_configuration_id: int

    class Settings:
        collection = "Metadata_model"

class ImagesModel(Document):
    """ Test Model """

    id: UUID
    original_image_path: str
    image_region_hand_path: Optional[str]
    image_region_palm_path: Optional[str]
    image_region_thumb_path: Optional[str]
    image_region_index_path: Optional[str]
    image_region_middle_path: Optional[str]
    image_region_ring_path: Optional[str]
    image_region_pinky_path: Optional[str]

    class Settings:
        collection = "ImagesDatabase"
