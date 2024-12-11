from pathlib import Path

from embeddings.embeddings_utils import calculate_embeddings_from_tensor_dict
import hand_normalization.src.main as normalization
from .regions_utils import PipelineDictKeys as Keys

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

    # TODO: delete when adding knn-search
    return dict_embedding

    ######## STEP 3: search nearest neighbours ###########################
    # TODO: Welche Vektordatenbank wird verwendet? 1 für Alter und 1 für Geschlecht oder beides in einer? -> 7 oder 14?

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
