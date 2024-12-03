import torch

from .image_utils import load_image_from_path_fragments, load_image_from_full_path, construct_image_path
from .models_utils import transforms_default, load_model

###############################################

# embeddings-calculation for an array of pictures via CNN and return via array

###############################################

def calculate_embeddings_from_full_paths(image_path_array, model=load_model) -> list[torch.Tensor]:
    """
    Calculates the embedding of every image in the given array of full image paths.

    Args:
        image_path_array (list[str]): list of image paths
        model: (DenseNet | ResNet) loaded (pytorch)-model with which the embedding is generated. Default: DenseNet121

    Returns:
        array of embeddings corresponding to input-array of images

    Example:
        `calculate_embeddings_from_path(["path/to/image/"], load_model(models_utils.CNNModel.DENSENET_121))`
    """
    loaded_images = []
    for image_path in image_path_array:
        loaded_images.append(load_image_from_full_path(image_path))
    return calculate_embeddings(loaded_images, model)


def calculate_embeddings_from_path_fragments(image_array, path_to_images, model=load_model) -> list[torch.Tensor]:
    """
    Calculates the embedding of every image in the given array of image names and a path to the images.

    Args:
        image_array: list[str] array of image file names
        path_to_images: (String) path to the image folder, where the images lie
        model: (DenseNet | ResNet) loaded (pytorch)-model with which the embedding is generated. Default: DenseNet121

    Returns:
        array of embeddings corresponding to input-array of images

    Example:
        `calculate_embeddings_from_path("image_name", "path/to/image/", load_model(models_utils.CNNModel.DENSENET_121))`
    """
    image_paths = []
    for image_name in image_array:
        image_paths.append(construct_image_path(image_name, path_to_images))
    return calculate_embeddings_from_full_paths(image_paths, model)


def calculate_embeddings(image_array: list[torch.Tensor], model=load_model) -> list[torch.Tensor]:
    """
    Calculates the embedding of every image in the given array of image tensors.

    Args:
        image_array: array of 3 dimensional RGB Tensors (3, H, W) with values of uint8 in range [0, 255]
        model: (DenseNet | ResNet) loaded (pytorch)-model with which the embedding is generated. Default: DenseNet121

    Returns:
        array of embeddings corresponding to input-array of images

    Example:
        `calculate_embeddings(image_array, load_model(models_utils.CNNModel.DENSENET_121))`
    """
    embeddings_array = []
    for image in image_array:
        embeddings_array.append(calculate_embedding(image, model))
    return embeddings_array


def calculate_embedding(image: torch.Tensor, model=load_model) -> torch.Tensor:
    """
    Uses the given model to generate the embedding of an image.
    Pushes model and data to gpu (cuda) if possible to enhance performance.
    Since the model does not get trained, no-grad (flag to stop backpropagation calculations) is used.
    Returns an embeddings-tensor of torch.Size([1, 1024]) (densenet) or torch.Size([1, 1000]) (resnet).

    Args:
        image: loaded image in form of 3 dimensional RGB Tensors (3, H, W) with values of uint8 in range [0, 255]
        model: (DenseNet | ResNet) loaded (pytorch)-model that generates embedding. Default: CNNModel.DenseNet121

    Returns:
        embedding-tensor of given image
    """

    device = choose_device()
    # use model on gpu if possible
    model = model.to(device)

    input_batch = preprocess_image(image)
    # push data to the same device as model
    input_batch.to(device)

    # prevent unnecessary backpropagation calculations
    with torch.no_grad():
        embedding = model(input_batch)

    # output embeddings-tensor
    return embedding


def preprocess_image(input_image: torch.Tensor, transforms=transforms_default) -> torch.Tensor:
    """
    Preprocesses 3D RGB image tensor (by using the transforms on it) into an input_batch for neural network.


    Args:
        input_image: 3 dimensional RGB Tensor of an image with values being uint8 in [0, 255]
        transforms: transforms used on the image

    Returns:
        tensor with values normalized to float values between 0 and 1
    """

    ## ready mini input_batch
    input_tensor = transforms(input_image)
    # debug: print(f"Input tensor: {input_tensor.shape}")

    # create a mini-batch as expected by the model
    # Unsqueeze: Returns a new tensor with a dimension of size one inserted at the specified position.
    # model expects 4D input, so unsqueeze turns 3D tensor to 4D tensor
    input_batch = input_tensor.unsqueeze(0)
    # debug: print(f"Input_Batch shape: {input_batch.shape}")
    return input_batch


###############################################
# helper functions


def choose_device() -> torch.device:
    """
    Chooses either 'cpu' or 'cuda' as device, depending on availability to run inference on.

    Returns:
        a context manager that changes the selected device (typically gpu or cpu depending on availability).
    """
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")
