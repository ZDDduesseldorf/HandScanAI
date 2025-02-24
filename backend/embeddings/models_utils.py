"""
Main Function: load_model() and CNNModel.
Do not use private create-functions outside of load_model().
"""

from enum import Enum
import torch
import torch.nn as nn
from torchvision import models
from torchvision.transforms import v2

from torchvision.models.densenet import DenseNet121_Weights
from torchvision.models.densenet import DenseNet169_Weights
from torchvision.models.resnet import ResNet50_Weights


###############################################
### MODELS
def _create_densenet121():
    """
    Helper Function:
    Loads densenet121 used for generating embeddings (tensors with 1024 dimensions, generated in second to last layer).

    Returns:
        A densenet121 model
    """
    return models.densenet121(weights=DenseNet121_Weights.DEFAULT)


def _create_densenet169():
    """
    Helper Function:
    Loads densenet169 used for generating embeddings (tensors with 1664 dimensions, generated in second to last layer).

    Returns:
        A densenet169 model
    """
    return models.densenet169(weights=DenseNet169_Weights.DEFAULT)


def _create_resnet50():
    """
    Helper Function:
    Loads resnet50 used for generating embeddings (tensors with 1000 dimensions, generated in second to last layer).

    Returns:
        A resnet50 model
    """
    return models.resnet50(weights=ResNet50_Weights.DEFAULT)


class CNNModel(Enum):
    DENSENET_121 = _create_densenet121
    DENSENET_169 = _create_densenet169
    RESNET_50 = _create_resnet50


def load_model(load_model_function: CNNModel = CNNModel.DENSENET_121) -> models.DenseNet | models.ResNet:
    """
    Loads pytorch cnn-model used for generating embeddings.
    Default-Model is densenet121 with embeddings-vector of 1024 dimensions.

    Embeddings are generated in second to last layer, after which the classifier (last layer)
    typically uses the embedding to produce its results.
    To access the embeddings without the classification, the named classifier-layer gets replaced
    with an identity layer to funnel through its input untouched.
    Additionally, the eval-flag prevents training and backpropagation.

    Returns:
        A cnn model (DenseNet or ResNet) without classifier that outputs embeddings of input images.
    """
    # load model via function
    model = load_model_function()
    # replace classifier with identity to access embeddings of preceeding layer (former input for classifier)
    model.classifier = nn.Identity()
    # inference mode instead of training mode
    model.eval()
    return model


###############################################
### TRANSFORMS
# Default-Transforms are chosen as the most suitable combination of typical transforms
# for the current pytorch models and our pipeline.
# Reference e.g. https://pytorch.org/hub/pytorch_vision_densenet/
# Those include
# * resizing (we do not resize to a bigger picture and crop to not lose details unnecessarily)
# * turning the image back into a vector and scaling it to values between o and 1
# Not currently used because it was deemed unnecessary:
# * normalization with Image_Net values v2.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])


# Image transformations that are used on every picture
transforms_default = v2.Compose(
    [
        # turns to "readable" image
        v2.ToImage(),
        # change size (optimal size for these CNN-models is 224x224), anti-aliasing: smoother edges)
        v2.Resize(size=(224, 224), antialias=True),
        # turn to float32, scale=True: scales values from 0 to 1])
        v2.ToDtype(torch.float32, scale=True),
    ]
)
