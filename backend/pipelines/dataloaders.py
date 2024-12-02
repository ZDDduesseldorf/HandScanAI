

# dataset_images
# input: folderpath
# load all paths
# return imagepath 
import os
from torch.utils.data import Dataset, DataLoader

class ImagePathDataset(Dataset):
    def __init__(self, folder_path):
        self.folder_path = folder_path
        # Get all file paths in the folder that have image file extensions
        self.image_paths = [
            os.path.join(folder_path, fname)
            for fname in os.listdir(folder_path)
            if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))
        ]

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        return self.image_paths[idx]

# dataset_image_with_metadata
# input: folderpath, metadatapath
# load paths
# load metadata csv
# link image with metadata entry
# return imagepath, metadata
import pandas as pd

class ImagePathWithCSV(Dataset):
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
        self.image_to_csv_entry = {
            row['imageName']: row.to_dict()
            for _, row in self.csv_data.iterrows()
        }

        # Get all file paths in the folder that have image file extensions
        self.image_paths = [
            os.path.join(folder_path, fname)
            for fname in os.listdir(folder_path)
            if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')) and fname in self.image_to_csv_entry
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
    
# dataset_regions
# input: folderpath, clustered_data = false
# load image or images paths 
# return imagepath or imagepaths

from collections import defaultdict


class DatasetRegions(Dataset):
    def __init__(self, folder_path, clustered_data=False):
        """
        Args:
            folder_path (str): Path to the folder containing images.
            clustered_data (bool): If True, return all images with the same UID together.
                                   If False, return images sequentially.
        """
        self.folder_path = folder_path
        self.clustered_data = clustered_data

        # Get all image file paths from the folder
        self.image_paths = [
            os.path.join(folder_path, fname)
            for fname in os.listdir(folder_path)
            if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
        ]

        # Parse image paths to group by UID
        self.uid_to_paths = defaultdict(list)
        for image_path in self.image_paths:
            filename = os.path.basename(image_path)
            uid, region = filename.split('_', 1)  # Split on the first underscore to get UID and region
            self.uid_to_paths[uid].append(image_path)

        # If clustered_data is True, use grouped UIDs for iteration
        if self.clustered_data:
            self.image_clusters = list(self.uid_to_paths.values())
        else:
            self.image_clusters = self.image_paths

    def __len__(self):
        """Returns the total number of items based on the mode."""
        return len(self.image_clusters)

    def __getitem__(self, idx):
        """
        Returns:
            - If clustered_data is True: List of image paths with the same UID.
            - If clustered_data is False: Single image path.
        """
        return self.image_clusters[idx]