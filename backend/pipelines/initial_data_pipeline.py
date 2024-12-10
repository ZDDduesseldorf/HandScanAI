from .datasets import ImagePathDataset, DatasetRegionClusters
from .initial_dataset_filter_pipeline import filter_11k_hands
from embeddings.embeddings_utils import calculate_embeddings_from_path_dict
import hand_normalization.src.main as normalization
from .regions_utils import PipelineDictKeys as Keys


### This pipeline is for filtering 11K dataset
def run_initial_data_pipeline(
    base_dataset_path, region_dataset_path, filter_initial_dataset=False, save_results_in_temp_folders=True
):
    ######## STEP 1: Create Base Dataset #################################
    # load images from 11K Dataset, validate and filter images
    if filter_initial_dataset:
        print("--------------- Validation: Load and filter initial dataset --------------------------------")
        # TODO: extract paths for config-file instead of hard-coding them here
        folder_path_initial_dataset = "path/to/image/folder"  # current dataset
        initial_csv_path = "path/to/csv"  # e.g. "J:\Dokumente\MMI\HandScanAI\Repo\HandScanAI\HandInfo.csv"
        base_dataset_path = ""  # e.g. "NewDataset" or "BaseDataset"
        new_csv_path = "CSV_filtered.csv"
        filter_11k_hands(
            folder_path=folder_path_initial_dataset,
            csv_path=initial_csv_path,
            new_dataset_path=base_dataset_path,
            new_csv_path=new_csv_path,
        )

    ######## STEP 2: Hand normalization #################################
    print("--------------- Hand-Normalization: Load dataset --------------------------------")
    # dataloader
    dataset_base = ImagePathDataset(base_dataset_path)

    print("--------------- Hand-Normalization: Normalize Images --------------------------------")
    # normalize images
    for path_dict in dataset_base:
        uuid = path_dict[Keys.UUID.value]
        path = path_dict[Keys.IMAGE_PATH.value]
        regions_dict = normalization.normalize_hand_image(uuid, path)

        # save normalized images (path: UUID_HandRegion)
        # for tests and debugs possible to comment this out
        if save_results_in_temp_folders:
            normalization.save_region_images(regions_dict, region_dataset_path)

    ######## STEP 3: Embeddings #################################
    print("--------------- Embeddings: Load dataset --------------------------------")
    dataset = DatasetRegionClusters(region_dataset_path)

    print("--------------- Embeddings: Calculate embeddings --------------------------------")
    # TODO: for test, delete when adding vector databases
    embeddings_all_test = []
    # dataset is a list
    # cluster is a dict {'uuid': str, 'image_paths': dict {HandRegions.key: path (str)}}
    for image_path_regions_cluster in dataset:
        embeddings_regions_dict = calculate_embeddings_from_path_dict(
            image_path_regions_cluster[Keys.IMAGE_PATHS_INITIAL.value]
        )
        # embeddings_all_test.append(test_embeddings)
        embeddings_dict = {
            Keys.UUID.value: image_path_regions_cluster[Keys.UUID.value],
            Keys.EMBEDDINGS.value: embeddings_regions_dict,
        }
        # TODO: for test, delete when adding vector databases
        embeddings_all_test.append(embeddings_dict)

    # TODO: for test, delete when adding vector databases
    return embeddings_all_test

    # TODO: in same for-loop: provide embeddings per region to vector trees (see following)

    ######## STEP 4: VECTOR DATABASE #################################
    # TODO: take embeddings from vector database
    # one vector database per Hand-region
    # save models (lokal folder/ database/ teams?)
