from pathlib import Path

from embeddings.embeddings_utils import calculate_embeddings_from_tensor_dict
import hand_normalization.src.main as normalization
from pipelines.data_utils import build_info_knn
from pipelines.distance_calculation import calculate_distance
from pipelines.inference_pipeline import _path_manager, get_image_path

# TODO: embeddings_csvs je Model erstellen
def run_scenarios_embeddings():
    # uuids der QueryBilder (bereits vorhanden, linke/rechte Hand in Datensatz vorhanden) 6-7 personen
    # 3 verschiedene modelle
    # k=10

    # wie vergleicht man die Ergebnisse am besten? niedrige Distanz nicht zwangsläufig gutes Ergebnis? 
    # -> Was ist gutes Ergebnis? (ähnliche Bild einer Person sollte ähnliches Embedding liefern)
    # von machen Personen viele Bilder drin von anderen weniger
    # These 1: nur 2 Bilder einer Person -> 1. Distanz 0, 2. anderes Bild
    # These 2: Augmentated Bilder -> Bilder der selben person am nächsten
    # alle Variablen hängen voneinander ab? Gridsearch?

    
def run_scenarios_classfiers():
    # uuids der QueryBilder (11k, eigene Bilder)
    # festgelegtes model
    # verschiedene ks (3,5,7,10)
    # verschiedene distanzmethoden ? (cosinus)
    # verschiedene Classfier pro Region (simple(mean, modus), gewichtung nach Distanz, Random Forest)
    # Ensemble Classifier (simple(mean, modus), Gewichtung nach Region)
    # Vergleich mit erwartetem Wert (Alter, Geschlecht)


def run_distance_pipeline(uuid, model, k):
    folder_path_query, _, embedding_csv_path, metadata_csv_path = _path_manager(testing=False)

    ######## STEP 0: build path to image #################################

    image_path = get_image_path(folder_path_query, uuid)

    ######## STEP 1: image normalization #################################

    dict_normalization = normalization.normalize_hand_image(image_path)

    ######## STEP 2: Calcualte embeddings ################################

    # calculate embeddings for each image from dict_normalization
    dict_embedding = calculate_embeddings_from_tensor_dict(dict_normalization, model)

    ######## STEP 3: search nearest neighbours ###########################

    dict_all_dist = calculate_distance(dict_embedding, k, embedding_csv_path)

    dict_all_info_knn = build_info_knn(metadata_csv_path, dict_all_dist)


    # TODO: Abspeicherung des dicts + metadaten in cvs oder alternativen



