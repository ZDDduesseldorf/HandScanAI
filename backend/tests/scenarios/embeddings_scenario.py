from pathlib import Path
import time

from embeddings.embeddings_utils import calculate_embeddings_from_tensor_dict
import hand_normalization.src.main as normalization
from pipelines.data_utils import build_info_knn_from_csv, build_info_knn_from_milvus
from pipelines.distance_calculation import calculate_cosine_distance
from pipelines.inference_pipeline import _path_manager
from utils.image_utils import get_image_path
from utils.logging_utils import save_nearest_neighbours_info
from utils.csv_utils import check_or_create_folder, check_file_exists, create_csv_with_header
from embeddings.models_utils import CNNModel, load_model
from pipelines.initial_data_pipeline import run_initial_data_pipeline
from utils.key_enums import PipelineDictKeys as Keys
from vectordb.milvus import drop_collection, search_embeddings_dict, milvus_default_search_params


# TODO: to execute the scenario_embeddings
"""def test_scenario_embeddings():"""
"""
Prerequisites:
        - original images in folder: app/media/BaseImages
        - region images in folder: app/media/RegionImages
        - if region images doesn't exists set normalize=True, save_images=True (for more information check docstring initial_data_pipeline)
    """
""" cleanup_tests()
run_scenarios_embeddings(setup=True)"""


def cleanup_tests():
    """
    Deletes the existing collections of models in Milvus
    """
    model_names = ["DENSENET_121", "DENSENET_169", "RESNET_50"]
    for name in model_names:
        drop_collection(name)


def scenario_path_manager():
    """
    creates the path to the folder for saving the result_csvs

    Returns:
        (str | Path): path to folder for saving the result_csvs
    """
    scenario_embeddings_path = Path(__file__).resolve().parent
    path_to_result_csv = scenario_embeddings_path / "result_csvs"

    return path_to_result_csv


def setup_scenario_structure(
    path_to_model_folder: (str | Path),
    model,
    model_name: str,
):
    """
    Initialisation of the setup for the scenario for each model. Creates a folder to save csvs if it does not already exist.
    Starts the initial_data_pipeline to calculate the embeddings for each region of each image in the dataset.
    Stops the time for calculating the embeddings for all images.

    Args:
        path_to_model_folder (str  |  Path): path to folder of the corresponding model in result_csv folder
        model (DenseNet | ResNet): CNN-model that generates the embeddings, uses default-Model
        model_name (str): name of the model used as key for milvus collection.
    """
    check_or_create_folder(path_to_model_folder)
    _, folder_path_region, _, _, folder_path_base = _path_manager(testing=False)
    start = time.time()

    run_initial_data_pipeline(
        folder_path_base,
        folder_path_region,
        path_to_model_folder,
        model,
        normalize=False,
        save_images=False,
        save_csvs=False,
        save_milvus=True,
        milvus_collection_name=model_name,
        model_name=model_name,
    )
    end = time.time()

    print("Dauer Initial:" + str((end - start) * 10**3) + "model: " + str(path_to_model_folder))


def check_or_create_nearest_neighbours_csv(path_to_csv_file: (str | Path)):
    """
    Check if file for saving the results of the nearest neighbour search already exists. If not creates them with correct header

    Args:
        path_to_csv_file (str  |  Path): path to file for saving the results of the nearest neighbour search.

    """
    if not check_file_exists(path_to_csv_file):
        header_nearest_neigbour = [
            Keys.UUID.value,
            Keys.REGION.value,
            Keys.NEIGHBOUR_UUID.value,
            Keys.SIMILARITY.value,
            Keys.AGE.value,
            Keys.GENDER.value,
        ]
        create_csv_with_header(path_to_csv_file, header_nearest_neigbour)


def run_scenarios_embeddings(setup: bool = False):
    """
    Defines models for embeddings calcuation, the number of nearest neighbours and the uuids for running the scenario.
    If setup is true, it creats for each model, the folders and files for saving the results and calculates the embedding for each region of each image.
    Then starts the distance_pipeline to find the nearest neighbours for each uuid and logs the result in csvs.

    Args:
        setup (bool, optional): flag for starting setup: creating folder, files and embeddings for each modell. Defaults to False.
    """
    path_to_result_csv = scenario_path_manager()
    models_dict = {
        "DENSENET_121": load_model(CNNModel.DENSENET_121),
        "DENSENET_169": load_model(CNNModel.DENSENET_169),
        "RESNET_50": load_model(CNNModel.RESNET_50),
    }
    k = 10
    uuid_list = [
        "d8c07bec-a8e5-464d-9332-6d180bcb0e25",
        "e8438076-49b2-49f2-b892-1a784c544ef6",
        "5fb19ec5-65d0-43ae-9460-8dac1040dbf1",
        "cb151d9a-f267-44fd-b8ad-e35a7ec6e43e",
        "78c579f8-b88c-42ff-8f02-21453d10e4a2",
        "976ad36d-0cc6-4c4e-b855-68db178da338",
        "898d31b4-7549-4f9b-88d1-83d8fd958fdd",
        "7c6c4cc9-7cc6-4cd8-9d79-05db814ee273",
        "790f8655-a97a-47e0-8c54-5c6b030d1d6c",
        "ca2b23a4-c9c2-46e4-b354-949326357ea0",
        "6d03ac69-49f3-4666-8185-27966ec852d1",
        "41564bb6-f474-4ddc-a95f-f1c4ff9815aa",
    ]
    for model_name, model in models_dict.items():
        if setup:
            model_csv_path = path_to_result_csv / model_name
            setup_scenario_structure(model_csv_path, model, model_name)
        for uuid in uuid_list:
            run_distance_pipeline(uuid, model_name, model, k, use_milvus=True)


def run_distance_pipeline(
    uuid: str, model_name: str, model, k: int, save_results: bool = True, use_milvus: bool = False
):
    """
    This function searches for the nearest neighbours of a search image by calculating the cosine distance/similarity.
    First, the image is loaded from the productive data and normalised.
    Then the embeddings are calculated with the specific model.
    Then the nearest neighbours can be searched using the embeddings of the base set stored in the csv or the vector database (Milvus).
    The csv is used to calculate the cosine distance and in the next step the similarity is calculated based on the distance.
    The cosine similarity is calculated using Milvus.
    The results of the similarity calculation can be saved and analysed in a csv file.

    Args:
        uuid (str):  Unique identifier for the image
        model_name (str): name of the model used as key for milvus collection.
        model (DenseNet | ResNet): CNN-model that generates the embeddings, uses default-Model
        k (int): number of nearest neighbours
        save_results (bool, optional): flag for writing the results in csvs. Defaults to True.
        use_milvus (bool, optional): Flag whether or not using milvus for nearest neighbour search . Defaults to False.
    """
    # productive data from app/media-folder
    _, _, _, metadata_csv_path, folder_path_base = _path_manager(testing=False)
    path_to_results_csv = scenario_path_manager()

    model_embedding_csv_path = path_to_results_csv / model_name

    ######## STEP 0: build path to image #################################

    image_path = get_image_path(folder_path_base, uuid)

    ######## STEP 1: image normalization #################################

    dict_normalization = normalization.normalize_hand_image(image_path)

    ######## STEP 2: Calcualte embeddings ################################

    # calculate embeddings for each image from dict_normalization
    dict_embedding = calculate_embeddings_from_tensor_dict(dict_normalization, model)

    ######## STEP 3: search nearest neighbours ###########################
    if not use_milvus:
        # for testing purposes/ if milvus is not available
        dict_all_dist = calculate_cosine_distance(dict_embedding, k, model_embedding_csv_path)

        dict_all_info_knn = build_info_knn_from_csv(metadata_csv_path, dict_all_dist)
    else:
        dict_all_similarities = search_embeddings_dict(dict_embedding, model_name, milvus_default_search_params, k)

        dict_all_info_knn = build_info_knn_from_milvus(metadata_csv_path, dict_all_similarities)

    # saving results in csvs
    if save_results:
        nearest_neighbour_csv_path = model_embedding_csv_path / "nearest_neighbours.csv"
        check_or_create_nearest_neighbours_csv(nearest_neighbour_csv_path)
        save_nearest_neighbours_info(uuid, dict_all_info_knn, nearest_neighbour_csv_path)
