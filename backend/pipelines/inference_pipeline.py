from pathlib import Path

from embeddings.embeddings_utils import calculate_embedding
import hand_normalization.src.main as normalization

# this file is used to generate the prediction of an image

######## STEP 0: image capture and validation in backend #############
# image is captured and saved in the following path:
# validation is checked: hand spread and hand visible

# UUID hier generiert und übergeben?

# result: image + metadata (UUID,....)


def run_inference_pipeline(uuid):
    temp_base_dir = Path(__file__).resolve().parent.parent
    ######## STEP 1: image normalization #################################

    # TODO: correct path, correct input image (with uuid)
    # path to specific image with UUID.jpg, UUID.png

    image_path = get_image_path(temp_base_dir, uuid)

    # segmentation of one image into 7 images as a dictionarie

    image_segements = normalization.segment_hand_image(image_path)

    # resize images to 224x224
    image_segmentes_resized = normalization.resize_images(image_segements)

    ######## STEP 2: Calcualte embeddings ################################

    # Übernahme dictionarie 'image_segmentes_resized' aus Step 1
    for element in image_segmentes_resized:
        # calculate embedding for each image
        image_tensor = element["image"]
        embedding = calculate_embedding(image_tensor)
        # add new element 'embedding' to dictionarie
        element["embedding"] = embedding

    return image_segmentes_resized

    ######## STEP 3: search nearest neighbours ###########################
    # TODO: Welche Vektordatenbank wird verwendet? 1 für Alter und 1 für Geschlecht oder beides in einer? -> 7 oder 14?
    # TODO: was ist k?

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
    extensions = [".png", ".jpg", ".jpeg", ".bmp"]
    folder_path_base = temp_base_dir / "tests" / "data" / "TestImages"
    for ext in extensions:
        image_path = folder_path_base / f"{uuid}{ext}"
        if image_path.exists():  # Überprüfen, ob die Datei existiert
            return image_path.resolve()
    return None  # Falls kein Bild gefunden wird
