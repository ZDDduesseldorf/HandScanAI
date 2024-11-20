# Expected:
# Takes one Array of seven pictures

# calculates embedding of each picture via CNN

# returns embeddings either via array or concatenated

############################################################

# imports
import torch
import torch.nn as nn
from torchvision import models

from torchvision.transforms import v2
from image_utils import load_image

## models
from torchvision.models.densenet import DenseNet121_Weights


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


## build CNN
def build_densenet_model():
    """
    Loads densenet model used for generating embeddings.
    Embeddings (vectors with 1024 dimensions) are generated in second to last layer, after which the classifier (last layer of the densenet) typically uses the embedding to produce its results.
    To access the embeddings without the classification, the named classifier-layer gets replaced with an identity layer to funnel through its input untouched.
    Additionally, the eval-flag prevents training and backpropagation.

    Returns:
        A densenet model without classifier that outputs embeddings of input images.
    """
    # load model via pytorch
    model = models.densenet121(weights=DenseNet121_Weights.DEFAULT)
    # replace classifier to access embeddings of preceeding layer (that would be the input for the classifier)
    model.classifier = nn.Identity()
    # user inference mode instead of training mode
    model.eval()
    return model


# input image is a tensor with rgb values, like the ones getting returned by load__image
def preprocess_image(input_image):
    """
    Preprocesses 3D RGB image tensor (by resizing the image and rescaling the rgb-values) into an input_batch that can be used by the neural network.
    TODO: are these transformations enough?

    Args:
        input_image: 3 dimensional RGB Tensor of an image with values being uint8 in [0, 255]

    Returns:
        tensor with values normalized to float values between 0 and 1
    """
    # image transformations that are used on every picture
    transforms_base = v2.Compose(
        [
            # turns to "readable" image
            v2.ToImage(),
            # change size (try different sizes, see optimal size for CNN-model used (this one is 224x224), anti-aliasing: smoother edges)
            v2.Resize(size=(224, 224), antialias=True),
            # turn to float32, scale=True: scales values from 0 to 1])
            v2.ToDtype(torch.float32, scale=True),
        ]
    )
    ## ready mini input_batch
    input_tensor = transforms_base(input_image)
    print(input_tensor)
    # TODO: why is this necessary?
    # create a mini-batch as expected by the model
    input_batch = input_tensor.unsqueeze(0)
    print(input_batch)
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
    input_batch = preprocess_image(loaded_image)
    # push data to the same device as model
    input_batch.to(device)

    # prevent unnecessary backpropagation calculations
    with torch.no_grad():
        embedding = model(input_batch)

    # output should be embedding of size 1024
    # print(embedding)

    return embedding


###############################################


# TODO: TEST, these are the results
# takes array of pictures, calculates embeddings, returns embeddings in an array
def calculate_embeddings(image_array, path_to_images):
    """
    Calculates the embedding of every image in the given image array.

    Args:
        image_array: (String) array of image file names
        path_to_images: (String) path to the image folder, where the image lies

    Returns:
        array of embeddings corresponding to imput-array of images
    """
    model = build_densenet_model()
    embeddings_array = []
    for image in image_array:
        embeddings_array.append(calculate_embedding(image, model, path_to_images))
    return embeddings_array


# TODO: return Umwandlung in Tensor (siehe Hilfsfunktion)
# Erst mal absprechen, was das result sein soll
# takes array of picutres, returns the embeddings as one concatenated embedding
def calculate_concatenated_embedding(image_array, path_to_images):
    """
    Calculates embeddings of every image in the array and concatenates them into one large embedding-vector.

    Args:
        image_array: (String) array of image file names
        path_to_images: (String) path to the image folder, where the image lies

    Returns:
        list of float-values (all float values of the embeddings of all pictures concatenated)
    """
    embeddings_array = calculate_embeddings(image_array, path_to_images)
    print(f"embeddings_array size: {len(embeddings_array)}")
    return concatenate_embeddings_array(embeddings_array)


# helper function, concatenates embeddings from array into one
def concatenate_embeddings_array(embeddings_array):
    """
    Concatenates an array of embeddings (arrays of float values) into one large embedding (array of float values).

    Args:
        arrays: A list of embeddings (lists containing float values).

    Returns:
        A single list containing all the float values from the input arrays.
    """
    super_empedding = []
    for embedding in embeddings_array:
        for tensor in embedding:
            super_empedding = super_empedding + tensor.tolist()
    return super_empedding
