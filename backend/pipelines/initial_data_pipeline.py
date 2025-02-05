from .datasets import ImagePathDataset, DatasetRegionClusters
from embeddings.embeddings_utils import calculate_embeddings_from_path_dict
import hand_normalization.src.main as normalization
from .regions_utils import PipelineDictKeys as Keys
from .csv_utils import create_region_csvs, add_embedding_dict_to_csv
from ann.milvus import add_embeddings_to_milvus


### This pipeline is for filtering 11K dataset
def run_initial_data_pipeline(base_dataset_path, region_dataset_path, csv_folder_path, save_results=True):
    ######## STEP 1: Hand normalization #################################
    print("--------------- Hand-Normalization: Load dataset --------------------------------")
    # dataloader
    dataset_base = ImagePathDataset(base_dataset_path)

    print("--------------- Hand-Normalization: Normalize Images --------------------------------")
    # normalize images
    for path_dict in dataset_base:
        uuid = path_dict[Keys.UUID.value]
        path = path_dict[Keys.IMAGE_PATH.value]
        regions_dict = normalization.normalize_hand_image(path)

        # save normalized images (path: UUID_HandRegion)
        # for tests and debugs possible to comment this out
        if save_results:
            normalization.save_region_images(uuid, regions_dict, region_dataset_path)

    ######## STEP 2: Embeddings #################################
    # # TODO: löschen nach Implementierung Vektordatenbank
    # if save_results:
    #     create_region_csvs(csv_folder_path)

    print("--------------- Embeddings: Load dataset --------------------------------")
    dataset = DatasetRegionClusters(region_dataset_path)
    # dataset is a list

    print("--------------- Embeddings: Calculate embeddings --------------------------------")
    # für Unit_test
    embeddings_all_test = []

    # cluster is a dict {'uuid': str, 'image_paths': dict {HandRegions.key: path (str)}}
    for image_path_regions_cluster in dataset:
        embeddings_regions_dict = calculate_embeddings_from_path_dict(
            image_path_regions_cluster[Keys.IMAGE_PATHS_INITIAL.value]
        )
        added_embedding = False
        if save_results:
            # TODO: Auskommentiert, da Milvus genutzt wird
            # added_embedding = add_embedding_dict_to_csv(csv_folder_path, uuid, embeddings_regions_dict)
            added_embedding = add_embeddings_to_milvus(uuid, embeddings_regions_dict)

        # ab hier für Unit-Tests
        embeddings_dict = {
            Keys.UUID.value: image_path_regions_cluster[Keys.UUID.value],
            Keys.EMBEDDINGS.value: embeddings_regions_dict,
            Keys.SAVED_EMBEDDINGS.value: added_embedding,
        }

        embeddings_all_test.append(embeddings_dict)

    # return wert für Unit-Test
    return embeddings_all_test
