import cv2
import os

from app.utils.uuid import generate_uuid
from pipelines.csv_utils import create_csv_with_header, add_entry_to_csv
from pipelines.datasets import ImagePathWithCSVDataset
from validation.validation_pipeline import validation_pipeline, is_validation_pipeline_valid


### This pipeline is for filtering 11K dataset into a first base dataset of hand images

# filters whole 11k dataset with validation_pipeline (valid hand image) and the hand being dorsal
# saves metadata in a csv and the images in a folder as a new base dataset
# image names are in the form of {UUID}.jpg


def filter_11k_hands(folder_path, csv_path, new_dataset_path, new_csv_path):
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

    for image_paths, csv_data in dataset_11k:
        image = cv2.imread(image_paths)
        is_valid = is_validation_pipeline_valid(validation_pipeline(image))

        # Check if its the dorsal side
        aspect_of_hand = csv_data["aspectOfHand"]
        is_dorsal = aspect_of_hand.split(" ", 1)[0] == "dorsal"

        if is_valid and is_dorsal:
            uuid = generate_uuid()
            ## save image at new_folder/UID.jpg
            image_path = os.path.join(new_dataset_path, uuid + ".jpg")
            cv2.imwrite(image_path, image)
            ## save metadata in new_csv
            csv_data["uuid"] = uuid
            csv_data["old_id"] = csv_data.pop("id")
            add_entry_to_csv(new_csv_path, csv_data)
