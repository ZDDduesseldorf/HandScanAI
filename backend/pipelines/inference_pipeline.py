from pathlib import Path
from scipy.spatial import distance
import statistics
import pandas as pd
import numpy as np

from embeddings.embeddings_utils import calculate_embeddings_from_tensor_dict, calculate_embeddings_from_path_dict
import hand_normalization.src.main as normalization

from .datasets import DatasetRegionClusters, ImagePathDataset
from .regions_utils import PipelineDictKeys as DictKeys
from .regions_utils import HandRegions as RegionKeys

# this file is used to generate the prediction of an image

# is triggered by the ‘Analyse Starten’ button in the frontend. Transfer of the uuid of the current image


# TODO pydoc
def run_inference_pipeline(uuid):
    """
    pipeline to classify age and gender based on the hand image

    Args:
        uuid (str): Unique identifier for the image

    Returns:
        actual: dict = {region(str): embedding(torch.Tensor)}

        later: age and gender prediction
    """
    temp_base_dir = Path(__file__).resolve().parent.parent
    ######## STEP 0: build path to image #################################

    image_path = get_image_path(temp_base_dir, uuid)

    ######## STEP 1: image normalization #################################

    dict_normalization = normalization.normalize_hand_image(image_path)

    ######## STEP 2: Calcualte embeddings ################################

    # calculate embeddings for each image from dict_regions
    dict_embedding = calculate_embeddings_from_tensor_dict(dict_normalization)

    ######## STEP 3: search nearest neighbours ###########################

    ## embeddings aller 4 embeddings
    # TODO: Anpassung an einlesen embeddings aus csv
    dict_all_embeddings = util_test_embeddings_calculate(temp_base_dir)
    # Schleife durch dict zur Berechnung jeder Distanz
    k = 3  # anzahl nächster Nachbarn
    dict_all_dist = calculate_distance(dict_embedding, dict_all_embeddings, k)

    dict_all_info_knn = build_info_knn(temp_base_dir, dict_all_dist)

    # 7 knn Abfragen für jede Region

    # bsp ballTree
    # input = embedding
    # dist, ind = hand_bt.query(input, k=2)
    # output: 2 Listen, dist=[dist, dist], ind = [embedding, embedding] von den 2 nächsten Nachbarn

    # search nearest neighbour in vectortree for each region

    # reslut: top 5? nearest neigbour for each region with distance

    ######## STEP 4: make a decision for prediction ######################
    # von embedding auf uuid zurückführen, um zugehöriges Alter festzustellen
    # TODO: Wo bekommen wir Alter/Geschlecht her? In Vektortree mit gespeichert oder ABfrage aus MongoDB?
    # random forest??
    age_dict = classify_age(dict_all_info_knn)
    gender_dict = classify_gender(dict_all_info_knn)
    return age_dict, gender_dict
    # kombination der 7 entscheidungsbäume jeder Region zu einem Ergebnis

    # Distanz, Alter/Geschlecht
    # Hand: (Alter, Distanz) = [(25, 0.5), (30, 0.8), (24, 0.4), (15, 0.1), (26, 0.6)]

    # TODO: TRaining RandomForest


# TODO: Verschieben in utils Datei
def get_image_path(temp_base_dir, uuid):
    # TODO: correct path to image_folder
    """
    Finds and returns the file path to an image based on its UUID and supported extensions.

    Args:
        temp_base_dir (Path): The base directory. Typically derived from the current file's location.
        uuid (str): Unique identifier for the image

    Returns:
        Path: The absolute path to the image file if found.
        None: If no file with the given UUID and extensions exists in the specified folder.
    """
    extensions = [".png", ".jpg", ".jpeg", ".bmp"]
    folder_path_base = temp_base_dir / "tests" / "data" / "TestBaseDataset"
    for ext in extensions:
        image_path = folder_path_base / f"{uuid}{ext}"
        if image_path.exists():
            return image_path.resolve()
    return None


# test funktion ohne csv aller embeddings
# TODO: nach Integration csv kann diese Funktion gelöscht werden
def util_test_embeddings_calculate(temp_base_dir):
    base_dataset_path = temp_base_dir / "tests" / "data" / "TestBaseDataset"

    dataset_base = ImagePathDataset(base_dataset_path)
    embeddings_dict = {
        RegionKeys.HAND_0.value: {},
        RegionKeys.HANDBODY_1.value: {},
        RegionKeys.THUMB_2.value: {},
        RegionKeys.INDEXFINGER_3.value: {},
        RegionKeys.MIDDLEFINGER_4.value: {},
        RegionKeys.RINGFINGER_5.value: {},
        RegionKeys.LITTLEFINGER_6.value: {},
    }

    for image_path_dict in dataset_base:
        dict_normalization = normalization.normalize_hand_image(image_path_dict[DictKeys.IMAGE_PATH.value])
        print("---inference---")
        print(dict_normalization)
        embeddings_regions_dict = calculate_embeddings_from_tensor_dict(dict_normalization)
        uuid = image_path_dict[DictKeys.UUID.value]

        for regionkey, embedding in embeddings_regions_dict.items():
            embeddings_dict[regionkey][uuid] = embedding

    return embeddings_dict


def calculate_distance(dict_embedding, dict_all_embeddings: dict, k):
    # return dict = {'Hand' : {'uuid': [56465, 1454514], 'distance': [0.1, 0.2], 'distance_ids_sorted' : [0,5]}}
    distance_dict = {
        RegionKeys.HAND_0.value: {},
        RegionKeys.HANDBODY_1.value: {},
        RegionKeys.THUMB_2.value: {},
        RegionKeys.INDEXFINGER_3.value: {},
        RegionKeys.MIDDLEFINGER_4.value: {},
        RegionKeys.RINGFINGER_5.value: {},
        RegionKeys.LITTLEFINGER_6.value: {},
    }

    # für jede Region distanzen berechnen
    for regionkey, embedding_dict in dict_all_embeddings.items():
        list_uuid = []
        list_embeddings = []
        for uuid, embedding in embedding_dict.items():
            list_uuid.append(uuid)
            list_embeddings.append(embedding[0])
        image_embedding = dict_embedding[regionkey]
        list_dist = distance.cdist(image_embedding, list_embeddings, "cosine")
        list_dist = list_dist[0]
        # sortiert distanzen und speichert deren indexe ab
        list_sorted_dist = np.argsort(list_dist)
        list_sorted_dist = list_sorted_dist[:k]

        distance_dict[regionkey][DictKeys.UUID.value] = np.array(list_uuid)
        distance_dict[regionkey]["distance"] = np.array(list_dist)
        distance_dict[regionkey]["distance_ids_sorted"] = np.array(list_sorted_dist)

    return distance_dict


def build_info_knn(temp_base_dir, dict_all_dist: dict):
    # return dict {'Hand' : dataframe(uuid, distance, age,gender)}
    dict_all_info_knn = {
        RegionKeys.HAND_0.value: {},
        RegionKeys.HANDBODY_1.value: {},
        RegionKeys.THUMB_2.value: {},
        RegionKeys.INDEXFINGER_3.value: {},
        RegionKeys.MIDDLEFINGER_4.value: {},
        RegionKeys.RINGFINGER_5.value: {},
        RegionKeys.LITTLEFINGER_6.value: {},
    }

    metadata_path = temp_base_dir / "tests" / "data" / "csv" / "Test_Hands_filtered_metadata.csv"
    metadata_df = pd.read_csv(metadata_path, sep=",")
    map_gender = {"female": 0, "male": 1}
    metadata_df.replace({"gender": map_gender}, inplace=True)

    for regionkey, dist_dict in dict_all_dist.items():
        region_df = pd.DataFrame(columns=[DictKeys.UUID.value, "distance", "age", "gender"])
        for index in dist_dict["distance_ids_sorted"]:
            uuid = dist_dict[DictKeys.UUID.value][index]
            dist = dist_dict["distance"][index]
            row = metadata_df.loc[metadata_df["uuid"] == uuid]
            # .iloc[0] notwendig sonst wird eindimensionale column gespeichert, nur Wert aus Zelle wird benötigt
            age = row["age"].iloc[0]
            gender = row["gender"].iloc[0]
            new_row = {DictKeys.UUID.value: uuid, "distance": dist, "age": age, "gender": gender}
            region_df = pd.concat([region_df, pd.DataFrame([new_row])])

        dict_all_info_knn[regionkey] = region_df

    return dict_all_info_knn


def classify_age(dict_all_info_knn):
    # return dict {'hand' : mean_age}
    dict_age = {}
    for regionkey, region_df in dict_all_info_knn.items():
        age_list = region_df["age"].to_list()
        age_mean = np.mean(age_list)
        dict_age[regionkey] = age_mean

    return dict_age


def classify_gender(dict_all_info_knn):
    # return dict {'hand' : mode_gender}
    dict_gender = {}
    for regionkey, region_df in dict_all_info_knn.items():
        gender_list = region_df["gender"].to_list()
        gender_mode = statistics.mode(gender_list)
        dict_gender[regionkey] = gender_mode

    return dict_gender
