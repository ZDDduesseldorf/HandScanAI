from validation.validation_pipeline import validation_pipeline, is_validation_pipeline_valid

from dataloaders import ImagePathDataset,ImagePathWithCSVDataset
from torch.utils.data import DataLoader

import cv2

from pipeline_utils import create_csv_with_header, add_entry_to_csv

from backend.app.utils import uuid
import os


### This pipeline is for filtering 11K dataset

# TODO: load images from 11K Dataset
# dataloader
folder_path = 'J:\Dokumente\MMI\HandScanAI\Repo\HandScanAI\TestImages' 
dataset_11k = ImagePathWithCSVDataset(folder_path)
dataloader_11k = DataLoader(dataset_11k, batch_size=1, shuffle=False)

# TODO: Validate/ filter images
# use validation pipeline (see websocket)
# save validated images in folder and metadata in csv
# image path: UUID.pdf (see websocket)
# result: base dataset
csv_path = "testcsv.csv"
csv_header = ["UID","old_id","age","gender",]
new_dataset_path = "NewDataset"
os.makedirs(new_dataset_path, exist_ok=True) 
create_csv_with_header(csv_path,csv_header)
for image_paths, csv_data in dataloader_11k:
    image = cv2.imread(image_paths, cv2.IMREAD_COLOR)
    if is_validation_pipeline_valid(validation_pipeline(image)):
        uid = uuid.generate_uuid()
        ## save image at new_folder/UID.jpg
        image_path = os.path.join(new_dataset_path, uid + ".jpg")
        cv2.imwrite(image_path, image)
        ## save metadata at new_csv new row
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
