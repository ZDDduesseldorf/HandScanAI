from embeddings.embeddings_utils import calculate_embeddings_from_tensor_dict
import hand_normalization.src.main as normalization
from .inference_pipeline import get_image_path, _path_manager
from utils.csv_utils import add_embedding_dict_to_csv, add_entry_to_csv
from utils.key_enums import PipelineAPIKeys, PipelineDictKeys
from utils.image_utils import copy_image_to_folder
from .data_utils import map_gender_int_to_string
from utils.logging_utils import logging_input_data

# before pipeline is started check is necessary to check the data and only if this is true start pipeline


def run_add_new_embeddings_pipeline(uuid, ground_truth_data: dict, testing=False):
    """
    pipeline to add classified and checked image to vektortree
    checking if the age and gender details are logical

    Args:
        uuid (str): Unique identifier for the image

    Returns:
        actual: dict = {region(str): embedding(torch.Tensor)}


    """
    folder_path_query, folder_path_region, embedding_csv_path, metadata_csv_path, folder_path_base = _path_manager(
        testing
    )

    ######## STEP 0: build path to image #################################

    image_path = get_image_path(folder_path_query, uuid)

    ######## STEP 1: image normalization #################################

    dict_normalization = normalization.normalize_hand_image(image_path)

    normalization.save_region_images(uuid, dict_normalization, folder_path_region)

    ######## STEP 2: Calcualte embeddings ################################

    # calculate embeddings for each image from dict_regions
    dict_embedding = calculate_embeddings_from_tensor_dict(dict_normalization)

    ######## STEP 3: Update datenbank ################################

    # TODO: normal return can be used for local testing, test and saving-methods need to be adjusted for
    # pipeline testing in a later issue to not actually save in the csv-files or set the saving back
    # while still using the correct testing-paths
    if testing:
        return True
    else:
        copied_image = copy_image_to_folder(uuid, folder_path_query, folder_path_base)
        added_metadata = add_entry_to_csv(
            metadata_csv_path,
            {
                PipelineDictKeys.UUID.value: uuid,
                PipelineDictKeys.AGE.value: ground_truth_data[PipelineAPIKeys.REAL_AGE.value],
                PipelineDictKeys.GENDER.value: map_gender_int_to_string(
                    ground_truth_data[PipelineAPIKeys.REAL_GENDER.value]
                ),
            },
        )
        added_embeddings = add_embedding_dict_to_csv(embedding_csv_path, uuid, dict_embedding)

        ### Logging ####
        logging_input_data(uuid, ground_truth_data)

        return added_embeddings and added_metadata and copied_image

    # für uns report sinnvoll mit vorhergesagtem und bestimmten Alter und Geschlecht, Timestamp?
