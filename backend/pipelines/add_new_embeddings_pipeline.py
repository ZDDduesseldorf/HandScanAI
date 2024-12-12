from pathlib import Path

from embeddings.embeddings_utils import calculate_embeddings_from_tensor_dict
import hand_normalization.src.main as normalization
from .inference_pipeline import get_image_path

# before pipeline is started check is necessary to check the data and only if this is true start pipeline


def run_add_new_embeddings_pipeline(uuid):
    """
    pipeline to add classified and checked image to vektortree
    checking if the age and gender details are logical

    Args:
        uuid (str): Unique identifier for the image

    Returns:
        actual: dict = {region(str): embedding(torch.Tensor)}


    """

    temp_base_dir = Path(__file__).resolve().parent.parent
    output_folder_path_base = temp_base_dir / "tests" / "data" / "TestRegionDataset"
    ######## STEP 0: build path to image #################################

    image_path = get_image_path(temp_base_dir, uuid)

    ######## STEP 1: image normalization #################################

    dict_normalization = normalization.normalize_hand_image(image_path)

    normalization.save_region_images(uuid, dict_normalization, output_folder_path_base)

    ######## STEP 2: Calcualte embeddings ################################

    # calculate embeddings for each image from dict_regions
    dict_embedding = calculate_embeddings_from_tensor_dict(dict_normalization)

    # TODO: delete when adding knn-search
    return dict_embedding

    ######## STEP 3: Update vektortree ################################

    # TODO: add embeddings to vektortree

    # TODO: calculate distances
