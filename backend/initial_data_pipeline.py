from validation.validation_pipeline import validation_pipeline, is_validation_pipeline_valid
from datasets import ImagePathDataset,ImagePathWithCSVDataset
from torch.utils.data import DataLoader

import cv2

from pipeline_utils import create_csv_with_header, add_entry_to_csv

from app.utils import uuid
import os


### This pipeline is for filtering 11K dataset

# TODO: load images from 11K Dataset
# dataloader
folder_path = 'J:\Dokumente\MMI\HandScanAI\Repo\HandScanAI\TestImages' 
dataset_11k = ImagePathWithCSVDataset(folder_path, csv_path="J:\Dokumente\MMI\HandScanAI\Repo\HandScanAI\HandInfo.csv")

# TODO: Validate/ filter images
# use validation pipeline (see websocket)
# save validated images in folder and metadata in csv
# image path: UUID.pdf (see websocket)
# result: base dataset
csv_path = "CSV_filter.csv"
csv_header = ["uuid","old_id","age","gender",]
new_dataset_path = "NewDataset"
os.makedirs(new_dataset_path, exist_ok=True) 
create_csv_with_header(csv_path,csv_header)
for image_paths, csv_data in dataset_11k:
    image = cv2.imread(image_paths)
    vp =validation_pipeline(image)
    print(vp)
    vvp = is_validation_pipeline_valid(vp)
    print(vvp)
    print("-----------------------------------------------")
    if vvp:
        uuid = uuid.generate_uuid()
        ## save image at new_folder/UID.jpg
        image_path = os.path.join(new_dataset_path, uuid + ".jpg")
        cv2.imwrite(image_path, image)
        ## save metadata at new_csv new row
        csv_data['uuid'] =  uuid
        csv_data['old_id'] = csv_data.pop('id')
        print(csv_data)
        add_entry_to_csv(csv_path,csv_data)
        print("------------------------------------------------- one image done -----------")
        break

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
