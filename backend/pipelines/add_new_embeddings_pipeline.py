from pathlib import Path

from embeddings.embeddings_utils import calculate_embedding
import hand_normalization.src.main as normalization
from pipelines.inference_pipeline import get_image_path

# this file is used to add the embedding of a new image to the vektortree

# After the image has been classified and checked to see if the age and gender details match
# the image can be added to the vektortree

# Step 1-3 are identical to the infernece_pipeline

def run_add_new_embeddings_pipeline(uuid):
    ######## STEP 0: image validation #################################

    # alle relevanten metadaten vorhanden?? (UUID, alter, geschlecht)
    # Unterschied links oder rechts?
    # Alter logisch?

    # TODO: Validation
    #if(check_metadata == True):

    temp_base_dir = Path(__file__).resolve().parent.parent
    ######## STEP 1: image normalization #################################

    # TODO: correct path, correct input image (with uuid)
    # path to specific image with UUID.jpg, UUID.png

    image_path = get_image_path(temp_base_dir, uuid)

    # segmentation of one image into 7 images as a dictionarie

    image_segements = normalization.segment_hand_image(image_path)

    # resize images to 224x224
    image_segmentes_resized = normalization.resize_images(image_segements)

    # TODO: Bilder lokal speichern? mit uuid_hand..
    normalization.save_image_with_name(image_segmentes_resized)

    ######## STEP 2: Calcualte embeddings ################################

    # Übernahme dictionarie 'image_segmentes_resized' aus Step 1
    for element in image_segmentes_resized:
        # calculate embedding for each image
        image_tensor = element["image"]
        embedding = calculate_embedding(image_tensor)
        #add new element 'embedding' to dictionarie
        element["embedding"] = embedding
    
    return image_segmentes_resized

    ######## STEP 3: Update vektortree ################################

    # TODO: add embeddings to vektortree

    # TODO: calculate distances


