from embeddings.embeddings_utils import calculate_embeddings_from_tensor_dict
import hand_normalization.src.main as normalization
from .inference_pipeline import get_image_path, _path_manager

# before pipeline is started check is necessary to check the data and only if this is true start pipeline


def run_add_new_embeddings_pipeline(uuid, testing=False):
    """
    pipeline to add classified and checked image to vektortree
    checking if the age and gender details are logical

    Args:
        uuid (str): Unique identifier for the image

    Returns:
        actual: dict = {region(str): embedding(torch.Tensor)}


    """
    folder_path_query, folder_path_region, _, _ = _path_manager(testing)

    ######## STEP 0: build path to image #################################

    image_path = get_image_path(folder_path_query, uuid)

    ######## STEP 1: image normalization #################################

    dict_normalization = normalization.normalize_hand_image(image_path)

    normalization.save_region_images(uuid, dict_normalization, folder_path_region)

    ######## STEP 2: Calcualte embeddings ################################

    # calculate embeddings for each image from dict_regions
    dict_embedding = calculate_embeddings_from_tensor_dict(dict_normalization)

    # TODO: delete when adding knn-search
    return dict_embedding

    ######## STEP 3: Update vektortree ################################

    # TODO: add embeddings to region_csv

    # TODO: Bild im richtigen Ordner speichern
    # TODO: Metadaten aus Frontend in Metadata.csv abspeichern
