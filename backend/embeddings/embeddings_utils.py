# Expected:
# Takes one Array of seven pictures

# calculates embedding of each picture via CNN

# returns embeddings either via array or concatenated

############################################################

# imports
import torch

from image_utils import load_image
import models_utils


# Takes one Array of seven pictures


###############################################


# calculates embedding of each picture via CNN
## choose cuda or cpu
def choose_device():
    """
    Chooses either 'cpu' or 'cuda' depending on availability to run inference on.

    Returns:
        A string 'cuda' or 'cpu' depending on availability.
    """
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


# TODO: transforms evtl ändern je nach model
# input image is a tensor with rgb values, like the ones getting returned by load__image
def preprocess_image(input_image, transforms=models_utils.transforms_default):
    """
    Preprocesses 3D RGB image tensor (by using the transforms on it) into an input_batch that can be used by the neural network.

    Args:
        input_image: 3 dimensional RGB Tensor of an image with values being uint8 in [0, 255]
        transforms: transforms used on the image

    Returns:
        tensor with values normalized to float values between 0 and 1
    """

    ## ready mini input_batch
    input_tensor = transforms(input_image)
    print(f"Input tensor: {input_tensor.shape}")

    # create a mini-batch as expected by the model
    # model expects 4D input, so unsqueeze turns 3D tensor to 4D tensor
    # Unsqueeze: Returns a new tensor with a dimension of size one inserted at the specified position.
    input_batch = input_tensor.unsqueeze(0)
    print(f"Input_Batch shape: {input_batch.shape}")
    return input_batch


def calculate_embedding(image_name, model, path_to_images):
    """
    Uses the given model to generate the embedding of an image.
    Pushes model and data to gpu (cuda) if possible to enhance performance.
    Since the model does not get trained, no-grad (flag to stop backpropagation calculations) is used.

    Args:
        image_name: name of the individual image-file
        model: loaded (pytorch)-model with which the embedding is generated
        path_to_images: path to the image folder, where the image lies

    Returns:
        embedding of torch.Size([1, 1024]) (example densenet)
    """
    device = choose_device()
    # use model on gpu if possible
    model = model.to(device)

    loaded_image = load_image(image_name, path_to_images)
    input_batch = preprocess_image(
        loaded_image,
    )
    # push data to the same device as model
    input_batch.to(device)

    # prevent unnecessary backpropagation calculations
    with torch.no_grad():
        embedding = model(input_batch)

    # output should be embedding of size 1024
    # print(embedding)

    return embedding


###############################################


# takes array of pictures, calculates embeddings, returns embeddings in an array
def calculate_embeddings(image_array, model, path_to_images):
    """
    Calculates the embedding of every image in the given image array.

    Args:
        image_array: (String) array of image file names
        model: loaded (pytorch)-model with which the embedding is generated
        path_to_images: (String) path to the image folder, where the image lies

    Returns:
        array of embeddings corresponding to imput-array of images
    """
    embeddings_array = []
    for image in image_array:
        embeddings_array.append(calculate_embedding(image, model, path_to_images))
    return embeddings_array


# Erst mal absprechen, was das result sein soll
# takes array of picutres, returns the embeddings as one concatenated embedding
def calculate_concatenated_embedding(image_array, model, path_to_images):
    """
    Calculates embeddings of every image in the array and concatenates them into one large embedding-vector.

    Args:
        image_array: (String) array of image file names
        path_to_images: (String) path to the image folder, where the image lies

    Returns:
        tensor of float-values (all float values of the embeddings of all pictures concatenated)
    """
    embeddings_array = calculate_embeddings(image_array, model, path_to_images)
    print(f"embeddings_array size: {len(embeddings_array)}")
    return concatenate_embeddings_array(embeddings_array)


# helper function, concatenates embeddings from array into one
def concatenate_embeddings_array(embeddings_array):
    """
    Concatenates an array of embeddings (tensors with float values) into one large embedding (tensor with float values).

    Args:
        embeddings_array: A list of embeddings (tensors of torch.Size([1, 1024])).

    Returns:
        A single tensor of [1, 7168] containing all the float values from the input embeddings. 1 is the row-count, 7168 is the column count of all the embeddings that have been concatenated.
    """
    # Concatenate along the second dimension (columns, dim=1)
    result = torch.cat(embeddings_array, dim=1)

    # Output: for 9 pictures, torch.Size([1, 9216]), for 7 torch.Size([1, 7168])
    print(result.shape)
    return result
