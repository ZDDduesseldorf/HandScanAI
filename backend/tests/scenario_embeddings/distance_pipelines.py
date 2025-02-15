from pathlib import Path
import time

from embeddings.embeddings_utils import calculate_embeddings_from_tensor_dict
import hand_normalization.src.main as normalization
from pipelines.data_utils import build_info_knn_from_milvus
from pipelines.distance_calculation import calculate_distance
from pipelines.inference_pipeline import _path_manager
from utils.image_utils import get_image_path
from utils.logging_utils import save_nearest_neighbours_info
from utils.csv_utils import check_or_create_folder, check_file_exists, create_csv_with_header
from embeddings.models_utils import CNNModel, load_model
from pipelines.initial_data_pipeline import run_initial_data_pipeline
from utils.key_enums import PipelineDictKeys as Keys


# TODO: zum Ausführen der distance_pipeline verwenden
"""def test_scenario_embeddings():
    run_scenarios_embeddings(setup=True)"""


def scenario_path_manager():
    scenario_embeddings_path = Path(__file__).resolve().parent
    path_to_result_csv = scenario_embeddings_path / "result_csvs"

    return path_to_result_csv


def setup_scenario_structure(
    path_to_model_folder,
    model,
    # model_name,
):
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
        save_milvus=False,
        # milvus_collection_name=model_name,
    )
    end = time.time()

    print("Dauer Initial:" + str((end - start) * 10**3) + "model: " + str(path_to_model_folder))


def check_or_create_nearest_neighbours_csv(path_to_csv_file):
    if check_file_exists(path_to_csv_file):
        return True
    else:
        header_nearest_neigbour = [
            Keys.UUID.value,
            Keys.REGION.value,
            Keys.NEIGHBOUR_UUID.value,
            Keys.DISTANCE.value,
            Keys.AGE.value,
            Keys.GENDER.value,
        ]
        create_csv_with_header(path_to_csv_file, header_nearest_neigbour)


# Erstellt Embeddings und Distanzberechnung pro Modell
def run_scenarios_embeddings(setup=False):
    path_to_result_csv = scenario_path_manager()
    models_dict = {
        "DENSENET_121": load_model(CNNModel.DENSENET_121),
        "DENSENET_169": load_model(CNNModel.DENSENET_169),
        "RESNET_50": load_model(CNNModel.RESNET_50),
    }
    k = 10
    uuid_list = [
        "4179975e-fca3-4beb-a2c9-10cc700ed5f4",
        "946e0eb9-5b0a-4e56-b99a-e665ac40de89",
        "218ce52f-4a15-42d9-8e1e-2d40492fc1ce",
        "23698a1f-d9ce-4df1-bd3a-e1de61a8f727",
        "516d1d19-61c4-42e9-b2dc-2697e0ecb743",
        "6976a5cd-276a-46d9-9e36-346c9bc0782a",
        "0dc125e4-a90e-45d6-8f7b-81538b1c96c5",
        "7116a897-a1a4-451e-a8fd-2e14cfeffb00",
        "12ebe903-747d-4294-b953-a1104f4f7042",
        "730cedf8-b717-403d-a464-148e45c00c3f",
        "6b7fe815-8a38-4fe8-a196-13b0c4a3d1a3",
        "25a13337-bb1d-4484-8135-066a6ac6876b",
    ]
    for model_name, model in models_dict.items():
        if setup:
            model_csv_path = path_to_result_csv / model_name
            setup_scenario_structure(model_csv_path, model)  # , model_name)
        for uuid in uuid_list:
            print(model_name, uuid)
            run_distance_pipeline(uuid, model_name, model, k)

    # wie vergleicht man die Ergebnisse am besten? niedrige Distanz nicht zwangsläufig gutes Ergebnis?
    # -> Was ist gutes Ergebnis? (ähnliche Bild einer Person sollte ähnliches Embedding liefern)
    # von machen Personen viele Bilder drin von anderen weniger
    # These 1: nur 2 Bilder einer Person -> 1. Distanz 0, 2. anderes Bild
    # These 2: Augmentated Bilder -> Bilder der selben person am nächsten
    # alle Variablen hängen voneinander ab? Gridsearch?


# def run_scenarios_classfiers():
# uuids der QueryBilder (11k, eigene Bilder)
# festgelegtes model
# verschiedene ks (3,5,7,10)
# verschiedene distanzmethoden ? (cosinus)
# verschiedene Classfier pro Region (simple(mean, modus), gewichtung nach Distanz, Random Forest)
# Ensemble Classifier (simple(mean, modus), Gewichtung nach Region)
# Vergleich mit erwartetem Wert (Alter, Geschlecht)


def run_distance_pipeline(uuid, model_name, model, k, save_results=True):
    # produktiv Daten aus Media Ordner
    folder_path_query, _, _, metadata_csv_path, folder_path_base = _path_manager(testing=False)
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

    dict_all_dist = calculate_distance(dict_embedding, k, model_embedding_csv_path)

    dict_all_info_knn = build_info_knn_from_milvus(metadata_csv_path, dict_all_dist)

    if save_results:
        nearest_neighbour_csv_path = model_embedding_csv_path / "nearest_neighbours.csv"
        check_or_create_nearest_neighbours_csv(nearest_neighbour_csv_path)
        save_nearest_neighbours_info(uuid, dict_all_info_knn, nearest_neighbour_csv_path)
