import numpy as np
import time
from .datasets import ImagePathDataset, DatasetRegionClusters
from embeddings.embeddings_utils import (
    calculate_embeddings_from_path_dict,
    _default_cnn_model_,
)
import hand_normalization.src.main as normalization
from utils.key_enums import PipelineDictKeys as Keys
from utils.csv_utils import create_region_csvs, add_embedding_dict_to_csv
from vectordb.milvus import add_embeddings_to_milvus, milvus_collection_name


def run_initial_data_pipeline(
    base_dataset_path,
    region_dataset_path,
    csv_folder_path,
    model=_default_cnn_model_,
    normalize=True,
    save_images=True,
    save_csvs=True,
    save_milvus=True,
    milvus_collection_name=milvus_collection_name,
    model_name="DENSENET_121",
) -> list:
    """
    This Funktion
    - takes a base dataset (containing images and the corresponding metadata as csv),
    - normalized the images into hand-region-images and saves them as bitmaps,
    - generates the images' embeddings and saves them per region (in csv-files).

    For testing purposes
    - it returns the generated embeddings per region and the corresponding uuid
    - it is used in scenario_embeddings to generate embeddings-csvs

    Args:
        base_dataset_path (str): path to base image folder
        region_dataset_path (str): path to folder where normalized images (region images) lie/ should be saved
        csv_folder_path (str): path to folder where metadata-csv lies and embeddings-csvs get saved
        model (DenseNet | ResNet): CNN-model that generates the embeddings, uses default-Model
        normalize (bool): choose whether or not to perform hand-normalization. Defaults to True. False skips normalization-step (e.g. for tests or in case normalized region images already exist and embeddings need to be re-generated)
        save_images (bool): choose whether or not to save the normalized images (hand-regions). Defaults to True. False skips saving step (e.g. for tests)
        save_csvs (bool): choose whether or not to save the embeddings in csv-files. Defaults to True. False skips the setup of the csvs and the saving of the embeddings in the csv-files.
        save_milvus (bool): choose whether or not to save the embeddings in a milvus vector database. Defaults to True. False skips the saving of the embeddings in the vector database.
        milvus_collection_name (str): name of the milvus-collection the embeddings are supposed to be saved in. Aside from test scenarios, the default collection name is used.

    Returns:
        embeddings_all_test (list): Only used for unit-tests. Contains a dictionary per image with its uuid and a bool whether or not saving the embeddings was successful.
    """
    ######## STEP 1: Hand normalization #######################################################################
    # skip this if normalized images already exist
    if normalize:
        print("--------------- Hand-Normalization: Load dataset --------------------------------")

        dataset_base = ImagePathDataset(base_dataset_path)

        print("--------------- Hand-Normalization: Normalize Images --------------------------------")

        for path_dict in dataset_base:
            uuid = path_dict[Keys.UUID.value]
            path = path_dict[Keys.IMAGE_PATH.value]
            regions_dict = normalization.normalize_hand_image(path)

            # save normalized images (path: UUID_HandRegion)
            # for tests and debugs possible to skip this
            if save_images:
                normalization.save_region_images(uuid, regions_dict, region_dataset_path)

    ######## STEP 2: Embeddings ################################################################################

    # load dataset (it's a list)
    dataset = DatasetRegionClusters(region_dataset_path)

    # for usage of csvs and test scenarios
    if save_csvs:
        create_region_csvs(csv_folder_path)

    # return value for unit tests
    embeddings_all_test = []

    # for progress display on command line
    logging_checkpoints = {int(len(dataset) * p) for p in np.arange(0.1, 1.1, 0.1)}  # Integer checkpoints
    start_time = time.time()

    print("--------------- Embeddings: Calculate and save embeddings ----------------------")

    # cluster is a dict {'uuid': str, 'image_paths': dict {HandRegions.key: path (str)}}
    for index, image_path_regions_cluster in enumerate(dataset):
        embeddings_regions_dict = calculate_embeddings_from_path_dict(
            image_path_regions_cluster[Keys.IMAGE_PATHS_INITIAL.value], model
        )
        added_embedding = False
        uuid = image_path_regions_cluster[Keys.UUID.value]

        # saving embeddings
        if save_csvs:
            # for usage of csvs and test scenarios
            added_embedding = add_embedding_dict_to_csv(csv_folder_path, uuid, embeddings_regions_dict)
        if save_milvus:
            added_embedding = add_embeddings_to_milvus(
                uuid, embeddings_regions_dict, milvus_collection_name, model_name
            )

        # for return value for unit tests
        embeddings_dict = {
            Keys.UUID.value: image_path_regions_cluster[Keys.UUID.value],
            # Keys.EMBEDDINGS.value: embeddings_regions_dict, # comment in for small tests, leave out for larger datasets
            Keys.SAVED_EMBEDDINGS.value: added_embedding,
        }

        # progress display on command line
        if index in logging_checkpoints:
            elapsed_time = time.time() - start_time
            print(
                f"{(index/len(dataset)*100):.0f}%: {index} of {len(dataset)} images done - Time elapsed: {elapsed_time:.2f} sec."
            )

        # return value for unit tests
        embeddings_all_test.append(embeddings_dict)

    # return value for unit tests
    return embeddings_all_test
