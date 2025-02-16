import cv2
import os

from utils.uuid_utils import generate_uuid
from utils.csv_utils import create_csv_with_header, add_entry_to_csv
from utils.image_utils import save_image_under_new_path
from pipelines.datasets import ImagePathWithCSVDataset
from validation.validation_pipeline import validation_pipeline, is_validation_pipeline_valid
import hand_normalization.src.main as normalization


def filter_11k_hands(folder_path: str, csv_path: str, new_dataset_path: str, new_csv_path: str):
    """
        This Funktion is for filtering 11K dataset into a first filtered dataset of hand images.
        Filters whole 11k dataset with validation_pipeline (valid hand image) and the hand being dorsal.
        Saves metadata in a csv and the images in a folder as a new filtered dataset.
        image names are in the form of {UUID}.jpg
    Args:
        folder_path (str): Path to folder with images of initial unfiltered dataset
        csv_path (str): Path to initial_metadata.csv e.g. "J:\Dokumente\MMI\HandScanAI\Repo\HandScanAI\HandInfo.csv"
        new_dataset_path (str): Path to folder for filtered Dataset
        new_csv_path (str): path to Metadata_filtered.csv

    """
    # load images from 11K Dataset
    dataset_11k = ImagePathWithCSVDataset(folder_path, csv_path=csv_path)
    csv_header = [
        "uuid",
        "old_id",
        "age",
        "gender",
        "skinColor",
        "accessories",
        "aspectOfHand",
        "imageName",
        "irregularities",
    ]

    # create files for saving
    os.makedirs(new_dataset_path, exist_ok=True)
    create_csv_with_header(new_csv_path, csv_header)

    for image_path, csv_data in dataset_11k:
        image = cv2.imread(image_path)
        is_valid = is_validation_pipeline_valid(validation_pipeline(image))
        normalization_succeeded = True
        try:
            normalization.normalize_hand_image(image_path)
        except (IndexError, ValueError, KeyError, cv2.error, TypeError):
            normalization_succeeded = False

        # Check if its the dorsal side
        aspect_of_hand = csv_data["aspectOfHand"]
        is_dorsal = aspect_of_hand.split(" ", 1)[0] == "dorsal"

        if is_valid and is_dorsal and normalization_succeeded:
            uuid = generate_uuid()
            ## save image at new_folder/UID.jpg
            new_image_path = os.path.join(new_dataset_path, uuid + ".jpg")
            save_image_under_new_path(image_path, new_image_path)
            ## save metadata in new_csv
            csv_data["uuid"] = uuid
            csv_data["old_id"] = csv_data.pop("id")
            add_entry_to_csv(new_csv_path, csv_data)
