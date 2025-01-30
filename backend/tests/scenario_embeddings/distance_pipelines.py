from pathlib import Path

from embeddings.embeddings_utils import calculate_embeddings_from_tensor_dict
import hand_normalization.src.main as normalization
from pipelines.data_utils import build_info_knn
from pipelines.distance_calculation import calculate_distance
from pipelines.inference_pipeline import _path_manager, get_image_path
from utils.logging_utils import save_nearest_neighbours_info
from utils.csv_utils import check_or_create_folder, check_file_exists, create_csv_with_header
from embeddings.models_utils import CNNModel, load_model
from pipelines.initial_data_pipeline import run_initial_data_pipeline
from utils.regions_utils import PipelineDictKeys as Keys


# TODO: zum Ausführen der distance_pipeline verwenden
"""def test_scenario_embeddings():
    # TODO: Zu testende Modelle und uuids in run_scenarios_embeddings anpassen
    run_scenarios_embeddings(setup=True)"""


def scenario_path_manager():
    scenario_embeddings_path = Path(__file__).resolve().parent
    path_to_result_csv = scenario_embeddings_path / "result_csvs"

    return path_to_result_csv


def setup_scenario_structure(path_to_model_folder, model):
    check_or_create_folder(path_to_model_folder)
    _, folder_path_region, _, _, folder_path_base = _path_manager(testing=False)
    run_initial_data_pipeline(
        folder_path_base,
        folder_path_region,
        path_to_model_folder,
        model,
        normalize=False,
        save_images=False,
        save_csvs=True,
    )


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
    uuid_list = ["514f53d0-6aab-4da1-b929-8f1dc0817289", "3ffd5331-da5d-4818-8af7-44869413714c"]
    for model_name, model in models_dict.items():
        if setup:
            model_csv_path = path_to_result_csv / model_name
            setup_scenario_structure(model_csv_path, model)
        for uuid in uuid_list:
            run_distance_pipeline(uuid, model_name, model, k)

    # uuids der QueryBilder (bereits vorhanden, linke/rechte Hand in Datensatz vorhanden) 6-7 personen
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
    folder_path_query, _, _, metadata_csv_path, _ = _path_manager(testing=False)
    path_to_results_csv = scenario_path_manager()

    model_embedding_csv_path = path_to_results_csv / model_name

    ######## STEP 0: build path to image #################################

    image_path = get_image_path(folder_path_query, uuid)

    ######## STEP 1: image normalization #################################

    dict_normalization = normalization.normalize_hand_image(image_path)

    ######## STEP 2: Calcualte embeddings ################################

    # calculate embeddings for each image from dict_normalization
    dict_embedding = calculate_embeddings_from_tensor_dict(dict_normalization, model)

    ######## STEP 3: search nearest neighbours ###########################

    dict_all_dist = calculate_distance(dict_embedding, k, model_embedding_csv_path)

    dict_all_info_knn = build_info_knn(metadata_csv_path, dict_all_dist)

    if save_results:
        nearest_neighbour_csv_path = model_embedding_csv_path / "nearest_neighbours.csv"
        check_or_create_nearest_neighbours_csv(nearest_neighbour_csv_path)
        save_nearest_neighbours_info(uuid, dict_all_info_knn, nearest_neighbour_csv_path)
