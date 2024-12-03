from validation.validation_pipeline import validation_pipeline, is_validation_pipeline_valid
from validation.hand_is_spread import hand_is_spread

from datasets import ImagePathDataset,ImagePathWithCSVDataset
from torch.utils.data import DataLoader

import cv2

from pipeline_utils import create_csv_with_header, add_entry_to_csv

from app.utils.uuid import generate_uuid
import os

### This pipeline is for filtering 11K dataset

# TODO: load images from 11K Dataset
# dataloader

# TODO: Validate/ filter images
# use validation pipeline (see websocket)
# save validated images in folder and metadata in csv
# image path: UUID.pdf (see websocket)
# result: base dataset
def filter_11k_hands(folder_path, new_dataset_path, csv_path):
    dataset_11k = ImagePathWithCSVDataset(folder_path, csv_path="J:\Dokumente\MMI\HandScanAI\Repo\HandScanAI\HandInfo.csv")
    csv_header = ["uuid","old_id","age","gender","skinColor","accessories", "aspectOfHand", "imageName", "irregularities"]

    # create files for saving
    os.makedirs(new_dataset_path, exist_ok=True) 
    create_csv_with_header(csv_path,csv_header)

    for image_paths, csv_data in dataset_11k:
        image = cv2.imread(image_paths)
        is_valid = is_validation_pipeline_valid(validation_pipeline(image))
        
        # Check if its the dorsal side
        aspectOfHand = csv_data["aspectOfHand"]
        is_dorsal = aspectOfHand.split(' ', 1)[0] == "dorsal"

        if is_valid and is_dorsal:
            uuid = generate_uuid()
            ## save image at new_folder/UID.jpg
            image_path = os.path.join(new_dataset_path, uuid + ".jpg")
            cv2.imwrite(image_path, image)
            ## save metadata in new_csv 
            csv_data['uuid'] =  uuid
            csv_data['old_id'] = csv_data.pop('id')
            add_entry_to_csv(csv_path,csv_data)

# TODO: hand-normalization
# dataloader
# save normalized images (path: UUID_HandRegion)
# provide Hand-regions as Enum or something similar to standardize path reading

# TODO: embeddings
# dataloader (loading with path)
# calculate embeddings
# provide embeddings per region to

# TODO: kNN (vector tree)
# one kNN Tree per Hand-region
# save models/trees (lokal folder/ teams?)




