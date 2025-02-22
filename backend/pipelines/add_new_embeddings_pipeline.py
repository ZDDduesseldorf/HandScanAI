from embeddings.embeddings_utils import calculate_embeddings_from_tensor_dict
import hand_normalization.src.main as normalization
from .inference_pipeline import _path_manager
from utils.csv_utils import add_embedding_dict_to_csv, add_entry_to_csv
from utils.key_enums import PipelineAPIKeys, PipelineDictKeys
from utils.image_utils import copy_image_to_folder, get_image_path
from .data_utils import map_gender_int_to_string
from utils.logging_utils import logging_input_data
from vectordb.milvus import add_embeddings_to_milvus, milvus_collection_name

# INFORMATION: only start pipeline if ground_truth_data was checked for plausibility


def run_add_new_embeddings_pipeline(
    uuid: str,
    ground_truth_data: dict[str, int],
    testing: bool = False,
    save_csvs: bool = True,
    save_milvus: bool = True,
    milvus_collection_name: str = milvus_collection_name,
):
    """
    Pipeline to process a classified and checked image by
    - saving its normalized region images
    - copying the image from the query-images into the folder for base-images
    - logging its metadata and adding its metadata to the metadata csv file
    - adding its embeddings to region-csv-files and/ or vector-database

    Args:
        uuid (str): Unique identifier for the image
        ground_truth_data (dict[str, int]): metadata containing age and gender
        testing (bool, optional): Flag whether or not to enable data saving. Defaults to False to enable unit testing.
        save_csvs (bool, optional): Flag whether or not to save embeddings in region-csv-files. Use instead of milvus, for testing or for data redundancy. Defaults to True.
        save_milvus (bool, optional): Flag whether or not to save embeddings in milvus-collection. Defaults to True.
        milvus_collection_name (str, optional): Name of the milvus collection. Defaults to milvus_collection_name.

    Returns:
        success (bool): True if image was copied, metadata was saved and embeddings were saved correctly
    """
    # use default paths depending on test- or production-mode
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

    ######## STEP 3: Update database ################################

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

        if save_csvs:
            # for testing reasons and data redundancy
            added_embeddings = add_embedding_dict_to_csv(embedding_csv_path, uuid, dict_embedding)
        if save_milvus:
            added_embeddings = add_embeddings_to_milvus(uuid, dict_embedding, milvus_collection_name)

        ### Logging ####
        # in case of errors, make sure logging has been setup correctly
        logging_input_data(uuid, ground_truth_data)

        return added_embeddings and added_metadata and copied_image

    # TODO: für uns report sinnvoll mit vorhergesagtem und bestimmten Alter und Geschlecht, Timestamp?
