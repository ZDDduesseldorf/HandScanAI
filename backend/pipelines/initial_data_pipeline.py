from pathlib import Path

from .datasets import ImagePathDataset, ImagePathWithCSVDataset, DatasetRegions
from .initial_dataset_filter_pipeline import filter_11k_hands
from embeddings.image_utils import construct_image_path
import hand_normalization.src.main as normalization


### This pipeline is for filtering 11K dataset
def run_initial_data_pipeline(filter_initial_dataset=False):
    # temp_base_dir geht bis backend
    temp_base_dir = Path(__file__).resolve().parent.parent

    ######## STEP 1: Create Base Dataset #################################
    # load images from 11K Dataset, validate and filter images
    # TODO: comment in when needed, update path to old csv in initial_dataset_filter_pipeline
    if filter_initial_dataset:
        # TODO: add correct path
        folder_path_initial_dataset = "path/to/image/folder"  # current dataset
        new_dataset_path = ""  # e.g. "NewDataset" or "BaseDataset"
        new_csv_path = "CSV_filtered.csv"
        filter_11k_hands(folder_path_initial_dataset, new_dataset_path, new_csv_path)

    ######## STEP 2: Hand normalization #################################
    # TODO: hand-normalization
    # path
    # TODO: correct path, correct input image (with uuid)
    folder_path_base = temp_base_dir / "tests" / "data" / "TestImages"
    print(folder_path_base)
    # dataloader
    dataset_base = ImagePathDataset(folder_path_base)
    print(dataset_base.image_paths)
    # save normalized images (path: UUID_HandRegion)
    normalized_dict = {}
    for path in dataset_base:
        images = normalization.segment_hand_image(path)
        images = normalization.resize_images(images)
        for image in images:
            # TODO: in hand-normalization keys korrigieren (siehe hand_regions)
            normalized_dict[image["name"]] = image["image"]
    # provide Hand-regions as Enum or something similar to standardize path reading
    print(normalized_dict)
    # TODO: abspeichern der Bilder unter dem korrekten Namen (where is the UUID?)

    ######## STEP 3: Embeddings #################################
    # TODO: embeddings
    print("--------------- Embeddings: Load dataset --------------------------------")
    # dataloader (loading with path)
    # path_to_images = #TODO (path to region images, see above)
    # dataset = DatasetRegions(path_to_region_images, clustered_data=True)

    print("--------------- Embeddings: Calculate embeddings --------------------------------")
    # calculate embeddings
    # for cluster in dataset:
    #    test_embeddings = embeddings_utils.calculate_embeddings_from_full_paths(cluster, models_utils.load_model())

    #    TODO: in same for-loop(?): provide embeddings per region to vector trees (see following)
    # TODO: or should embeddings be saved to be loaded into vector trees?

    ######## STEP 4: Search Trees #################################
    # TODO: kNN (vector tree)
    # one kNN Tree per Hand-region
    # save models/trees (lokal folder/ teams?)
