from pipelines.initial_dataset_filter_pipeline import filter_11k_hands
from pipelines.datasets import ImagePathDataset, ImagePathWithCSVDataset, DatasetRegions


### This pipeline is for filtering 11K dataset

######## STEP 1: Create Base Dataset #################################
# load images from 11K Dataset, validate and filter images
# TODO: comment in when needed, update path to old csv in initial_dataset_filter_pipeline
# folder_path = 'path/to/image/folder' # current dataset
# new_dataset_path = "NewDataset" or "BaseDataset"
# new_csv_path = "CSV_filter.csv"
# filter_11k_hands(folder_path, new_dataset_path, new_csv_path)


######## STEP 2: Hand normalization #################################
# TODO: hand-normalization
# dataloader
# save normalized images (path: UUID_HandRegion)
# provide Hand-regions as Enum or something similar to standardize path reading


######## STEP 3: Embeddings #################################
# TODO: embeddings
print("--------------- Embeddings: Load dataset --------------------------------")
# dataloader (loading with path)
#path_to_images = #TODO (path to region images, see above)
#dataset = DatasetRegions(path_to_region_images, clustered_data=True)

print("--------------- Embeddings: Calculate embeddings --------------------------------")
# calculate embeddings
#for cluster in dataset:
#    test_embeddings = embeddings_utils.calculate_embeddings_from_full_paths(cluster, models_utils.load_model())

#    TODO: in same for-loop(?): provide embeddings per region to vector trees (see following)
# TODO: or should embeddings be saved to be loaded into vector trees?


######## STEP 4: Search Trees #################################
# TODO: kNN (vector tree)
# one kNN Tree per Hand-region
# save models/trees (lokal folder/ teams?)




