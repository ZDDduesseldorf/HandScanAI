"""
This module contains datasets that handle the loading and iterating of large quantities of images,
as is the case with any image folder used in the context of this application.

They are used in the initial_dataset_filter_pipeline, the initial_data_pipeline as well as test-scenarios that similarly handle whole datasets.
"""

from collections import defaultdict
import os
import pandas as pd
from torch.utils.data import Dataset
from utils.key_enums import PipelineDictKeys


class ImagePathDataset(Dataset):
    """
    This dataset takes a path to a folder containing original images (images with the filename-scheme {UUID}.[ext}]).

    It is typically used to load the paths to the images contained in BaseImages (e.g. in initial_data_pipeline).

    Its return value per list-item is a dict:
    ```
    {
        'image_path': # absolute path to an image in the folder,
        'uuid': # unique identifier of the image extracted from its filename
    }
    ```
    """

    def __init__(self, folder_path):
        self.folder_path = folder_path
        # Get all file paths in the folder that have image file extensions
        self.image_paths = [
            {
                PipelineDictKeys.IMAGE_PATH.value: os.path.join(folder_path, fname),
                PipelineDictKeys.UUID.value: extract_uuid_from_filename(fname),
            }
            for fname in os.listdir(folder_path)
            if fname.lower().endswith((".png", ".jpg", ".jpeg", ".bmp"))
        ]

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        return self.image_paths[idx]


class ImagePathWithCSVDataset(Dataset):
    """
    This dataset takes a path to a folder containing images and a path to a csv containing metadata corresponding to the images.

    It is typically used to load the paths and metadata of the images contained in an external dataset (like 11K) to filter them for useful entries (e.g. in initial_dataset_filter_pipeline).

    Its return value per list-item is a Tuple (str, dict); an image path and its corresponding CSV row entry

    Example for use/ test:
        ```
        folder_path = 'TestImages'
        csv_path = 'HandInfo.csv'
        dataset = ImagePathWithCSVDataset(folder_path, csv_path)
        ```

        Iterate over the Dataset
        ```
        for image_path, csv_entry in dataset:
            print("Image Path:", image_path)
            print("CSV Entry:", csv_entry)
        ```
    """

    def __init__(self, folder_path, csv_path):
        """
        Args:
            folder_path (str): Path to the folder containing images.
            csv_path (str): Path to the CSV file containing additional data.
        """
        self.folder_path = folder_path

        # Load the CSV file into a pandas DataFrame
        self.csv_data = pd.read_csv(csv_path)

        # Create a dictionary mapping image file names to corresponding row entries
        self.image_to_csv_entry = {row["imageName"]: row.to_dict() for _, row in self.csv_data.iterrows()}

        # Get all file paths in the folder that have image file extensions
        self.image_paths = [
            os.path.join(folder_path, fname)
            for fname in os.listdir(folder_path)
            if fname.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")) and fname in self.image_to_csv_entry
        ]

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        """
        Returns the image path and corresponding CSV entry at index `idx`.
        Args:
            idx (int): Index of the image path to retrieve.
        Returns:
            Tuple (str, dict): Image path and corresponding CSV row entry.
        """
        image_path = self.image_paths[idx]
        image_name = os.path.basename(image_path)  # Get the image file name
        csv_entry = self.image_to_csv_entry.get(image_name, None)  # Get the corresponding CSV entry
        return image_path, csv_entry


class DatasetRegionClusters(Dataset):
    """
    This dataset takes a path to a folder containing region images (images with the filename-scheme {UUID}_{region}.[ext}]).

    It is typically used to load the paths to the images contained in RegionImages (e.g. in initial_data_pipeline).

    Its return value per list-item is a is a dict:
    ```
        {
            'uuid': str,
            'image_paths': dict {
                region_key (str): image_path (str)
            }
        }
    ```

    Example for use/ test:
        ```
        folder_path = 'TestRegionDataset'
        dataset = DatasetRegionClusters(folder_path)
        ```

        Iterate over the Dataset
        ```
        for image_paths in dataset:
            # prints an array of all imagepaths with the same uuid each iteration
            print("Image Path:", image_path)
        ```
    """

    def __init__(self, folder_path: str):
        """
        Args:
            folder_path (str): Path to the folder containing images.
        """
        self.folder_path = folder_path

        # Get all image file paths from the folder
        self.image_paths = [
            os.path.join(self.folder_path, fname)
            for fname in os.listdir(self.folder_path)
            if fname.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))
        ]

        # Parse image paths to group by UUID
        self.uuid_to_paths = defaultdict(lambda: defaultdict(str))
        for image_path in self.image_paths:
            filename = os.path.basename(image_path)
            uuid, region = extract_uuid_and_region_from_filename(filename)
            # dict of key=uuid, value=dict of key=region, value=path
            self.uuid_to_paths[uuid][region] = image_path

            # uuid_to_paths is a dict (uuid) with values dict (region: paths)
            # iterate over uuid -> region_dict and append the entries as new dicts
            # results in list of dicts{ uuid: str, image_paths: dict{ region_key: path}}
            self.image_clusters = [
                {PipelineDictKeys.UUID.value: uuid, PipelineDictKeys.IMAGE_PATHS_INITIAL.value: value}
                for uuid, value in self.uuid_to_paths.items()
            ]

    def __len__(self):
        """Returns the total number of items."""
        return len(self.image_clusters)

    def __getitem__(self, idx):
        """
        Returns:
        ```
        dict {
            'uuid': str,
            'image_paths': dict {
                region_key (str): image_path (str)
            }
        }
        ```
        """
        # key=uuid, value=dict of key=region, value=path
        return self.image_clusters[idx]


def extract_uuid_from_filename(filename: str) -> str:
    """
    This function extracts the uuid from a filename of the format {UUID}.{ext}.

    Args:
        filename (str): filename of an image of the format {UUID}.{ext}

    Returns:
        uuid (str): uuid of the image, used to identify the image and link it to its corresponding region images and metadata
    """
    uuid, _ = filename.split(".", 1)  # Split on the first underscore to get UUID and region
    return uuid


def extract_uuid_and_region_from_filename(filename: str) -> tuple[str, str]:
    """
    This function extracts the uuid and the region from a filename of the format {UUID}_{region}.{ext}.

    Args:
        filename (str): filename of an image of the format {UUID}_{region}.{ext}

    Returns:
        (uuid, region) (tuple[str, str]): uuid and region of the image
    """
    uuid, region = filename.split("_", 1)  # Split on the first underscore to get UUID and region
    region, _ = region.split(".", 1)
    return uuid, region
