from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime, timezone
from uuid import UUID


class CameraConfiguration(Document):
    """ Camera Configuration Document """

    configuration_id : int
    camera_type: str
    camera_position: str
    height: int
    width: int


class MetadataModel(Document):
    """ MetadataModel """
    id: UUID
    age: int
    age_confirmed: Optional[bool] = False 
    gender: str
    gender_confirmed: Optional[bool] = False

    person_id: Optional[int] = -1
    skin_colour: Optional[str] = "not specified" 
    accessories: Optional[int] = -1
    nail_polish: Optional[int] = -1
    aspect_of_hand: Optional[str] = "not specified" 
    eleven_k_hands_image_name: Optional[str] = "not specified" 
    irregularities: Optional[int] = -1

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    camera_configuration_id: int

    class Settings:
        collection = "MetadataModel"

class ImagesModel(Document):
    """ Test Model """

    id: UUID
    original_image_path: str
    image_region_hand_path: Optional[str] = "not specified" 
    image_region_palm_path: Optional[str] = "not specified" 
    image_region_thumb_path: Optional[str] = "not specified" 
    image_region_index_path: Optional[str] = "not specified" 
    image_region_middle_path: Optional[str] = "not specified" 
    image_region_ring_path: Optional[str] = "not specified" 
    image_region_pinky_path: Optional[str] = "not specified" 

    class Settings:
        collection = "ImagesDatabase"
