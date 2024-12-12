import pytest
import torch
from pathlib import Path
from embeddings import embeddings_utils

# Run file in manage.py
# Command: python manage.py anntree

def run_anntree():
    print("test")

    temp_base_dir = Path(__file__).resolve().parent.parent
    folder_path_region = temp_base_dir / "tests" / "data" / "TestRegionDataset"


    def test_calculate_embeddings_from_dict(path_to_region_images: str):
        uuid = '614f53d0-6aab-4da1-b929-8f1dc0817289'
        region_dict = {
            "Hand": path_to_region_images + "\\614f53d0-6aab-4da1-b929-8f1dc0817289_Hand.jpg",
            "HandBody": path_to_region_images + "\\614f53d0-6aab-4da1-b929-8f1dc0817289_HandBody.jpg",
            "IndexFinger": path_to_region_images + "\\614f53d0-6aab-4da1-b929-8f1dc0817289_IndexFinger.jpg",
            "LittleFinger": path_to_region_images + "\\614f53d0-6aab-4da1-b929-8f1dc0817289_LittleFinger.jpg",
            "MiddleFinger": path_to_region_images + "\\614f53d0-6aab-4da1-b929-8f1dc0817289_MiddleFinger.jpg",
            "RingFinger": path_to_region_images + "\\614f53d0-6aab-4da1-b929-8f1dc0817289_RingFinger.jpg",
            "Thumb": path_to_region_images + "\\614f53d0-6aab-4da1-b929-8f1dc0817289_Thumb.jpg",
        }
        embeddings_dict: dict[str, torch.Tensor] = embeddings_utils.calculate_embeddings_from_path_dict(region_dict)
        # expect the result dict to have the same amount of keys as the input dict
        assert len(embeddings_dict) == len(region_dict)
        # expect the result dict to have the same keys as the input dict
        assert embeddings_dict.keys() == region_dict.keys()
        # expect the embedding-value to have the correct length for the densenet used per default (1024)
        assert embeddings_dict["Hand"].shape[1] == 1024


