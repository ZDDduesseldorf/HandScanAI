from numpy import ndarray
import torch
from sklearn.preprocessing import normalize

from utils.image_utils import load_image_from_full_path
from .models_utils import transforms_default, load_model

###############################################

# embeddings-calculation for an array of pictures via CNN and return via array

###############################################

# Default-Model (Densenet121)
# TODO: for change of model/ default model, always update model name as well
_default_cnn_model_, default_model_name = load_model(), "DENSENET_121"

###############################################


def calculate_embeddings_from_tensor_dict(regions_dict: dict, model=_default_cnn_model_) -> dict[str, ndarray]:
    """
    Calculates the embedding of every image in the given dict of region keys and image-tensor values.
    The ndarrays (here called image_tensors) in regions_dict represent 3-dimensional RGB arrays (3 x H x W) of images with values being uint8 in [0, 255].

    Args:
        regions_dict (dict[str, ndarray]): dict of region keys and image_tensor values
        model (DenseNet | ResNet): loaded (pytorch)-model with which the embedding is generated. Default: DenseNet121

    Returns:
        embeddings_dict (dict[str, ndarray]): dict of region keys and of embeddings (float arrays) corresponding to input dict

    Example:
        `calculate_embeddings_from_path_dict(regions_dict, load_model(models_utils.CNNModel.DENSENET_121))`
        `calculate_embeddings_from_path_dict(regions_dict)`
    """
    embeddings_dict = {}
    for region_key, image_tensor in regions_dict.items():
        embeddings_dict[region_key] = calculate_embedding(image_tensor, model)
    return embeddings_dict


def calculate_embeddings_from_path_dict(regions_dict: dict[str, str], model=_default_cnn_model_) -> dict[str, ndarray]:
    """
    Calculates the embedding of every image in the given dict of region keys and image-path values.

    Args:
        regions_dict (dict[str, str]): dict of region keys and image-path values
        model (DenseNet | ResNet): loaded (pytorch)-model with which the embedding is generated. Default: DenseNet121

    Returns:
        embeddings_dict (dict[str, ndarray]): dict of region keys and of embeddings (float arrays) corresponding to input dict

    Example:
        `calculate_embeddings_from_path_dict(regions_dict, load_model(models_utils.CNNModel.DENSENET_121))`
        `calculate_embeddings_from_path_dict(regions_dict)`
    """
    embeddings_dict = {}
    for region_key, image_path in regions_dict.items():
        image = load_image_from_full_path(image_path)
        embeddings_dict[region_key] = calculate_embedding(image, model)
    return embeddings_dict


def normalize_embedding(embedding: ndarray) -> ndarray:
    """
    Normalizes input vectors individually to unit norm (vector length) by scaling them.
    "This process can be useful if quadratic form such as the dot-product is used, e.g. in calculating similarity/ distance between vectors." (scikit-learn.org)

    L2 is the used (and default) norm because "the dot product of two l2-normalized TF-IDF vectors is the cosine similarity of the vectors and is the base similarity metric for the Vector Space Model commonly used by the Information Retrieval community."

    Sources:
    - https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.Normalizer.html
    - https://scikit-learn.org/stable/modules/preprocessing.html#normalization

    Args:
        embedding (ndarray): embedding-tensor of given image

    Returns:
        normalized_embedding (ndarray): normalized (values between -1 and 1) 1-dimensional embeddings-vector that retains the length of the respective model's embeddings
    """
    # extract the feature vector
    feature_vector = embedding.squeeze()
    # Scale input vectors individually to unit norm (vector length, between 1 and -1). This process can be useful if you plan to use a quadratic form such as the dot-product
    return normalize(feature_vector.reshape(1, -1), norm="l2").flatten()


def calculate_embedding(image: (torch.Tensor | ndarray), model=_default_cnn_model_) -> ndarray:
    """
    Uses the given model to generate the embedding of an image.
    Pushes model and data to gpu (cuda) if possible to enhance performance.
    Since the model does not get trained, no-grad (flag to stop backpropagation calculations) is used.
    Returns a normalized embeddings-tensor of length 1024 (for default model) and with values between 1 and -1.

    Args:
        image (torch.Tensor | ndarray): image as 3 dimensional RGB Tensor/array (3, H, W) with values of uint8 in range [0, 255]
        model (DenseNet | ResNet): loaded (pytorch)-model that generates embedding. Default: CNNModel.DenseNet121

    Returns:
        normalized_embedding (ndarray): normalized (values between -1:1) 1-dimensional embeddings-vector
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
    return normalize_embedding(embedding)


def preprocess_image(input_image: (torch.Tensor | ndarray), transforms=transforms_default) -> torch.Tensor:
    """
    Preprocesses 3D RGB image tensor (by using the transforms on it) into an input_batch for neural network.


    Args:
        input_image (torch.Tensor | ndarray): 3 dimensional RGB Tensor of an image with values being uint8 in [0, 255]
        transforms: transforms used on the image

    Returns:
        input_batch (torch.Tensor): tensor with values normalized to float values between 0 and 1
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
        device (torch.device): a context manager that changes the selected device (typically gpu or cpu depending on availability).
    """
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")
