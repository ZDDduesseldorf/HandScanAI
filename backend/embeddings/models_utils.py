import torch
import torch.nn as nn
from torchvision import models
from torchvision.transforms import v2

from torchvision.models.densenet import DenseNet121_Weights
from torchvision.models.densenet import DenseNet169_Weights
from torchvision.models.resnet import ResNet50_Weights


# image transformations that are used on every picture
transforms_default = v2.Compose(
    [
        # turns to "readable" image
        v2.ToImage(),
        # change size (try different sizes, see optimal size for CNN-model used (this one is 224x224), anti-aliasing: smoother edges)
        v2.Resize(size=(224, 224), antialias=True),
        # turn to float32, scale=True: scales values from 0 to 1])
        v2.ToDtype(torch.float32, scale=True),
    ]
)

### DENSENET


def build_densenet121_model():
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


# image transformations specifically for densenet that are used on every picture
# see https://pytorch.org/hub/pytorch_vision_densenet/
transforms_densenet = v2.Compose(
    [
        # turns to "readable" image (like Image.open(image) instead of load_image)
        v2.ToImage(),
        # INFO: densenet transforms use first resize then crop. We won't do that right now to not lose unnecessary information. Maybe changed later.
        # v2.Resize(size=(256)),
        # v2.CenterCrop(224),
        # instead just resize (maybe try different sizes, optimal size per docu for this one is 224x224, anti-aliasing: smoother edges)
        v2.Resize(size=(224, 224), antialias=True),
        # deprecated
        # v2.ToTensor(),
        # turn to float32, scale=True: scales values from 0 to 1])
        v2.ToDtype(torch.float32, scale=True),
        # Normalization values of Image_Net (recommended)
        # TODO: does this make sense to use here or is this only relevant for fine-tuning/ transfer-learning?
        # v2.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)


def build_densenet169_model():
    """
    Loads densenet model used for generating embeddings.
    Embeddings (vectors with 1024 dimensions) are generated in second to last layer, after which the classifier (last layer of the densenet) typically uses the embedding to produce its results.
    To access the embeddings without the classification, the named classifier-layer gets replaced with an identity layer to funnel through its input untouched.
    Additionally, the eval-flag prevents training and backpropagation.

    Returns:
        A densenet model without classifier that outputs embeddings of input images.
    """
    # load model via pytorch
    model = models.densenet169(weights=DenseNet169_Weights.DEFAULT)
    # replace classifier to access embeddings of preceeding layer (that would be the input for the classifier)
    model.classifier = nn.Identity()
    # user inference mode instead of training mode
    model.eval()
    return model


### RESNET


def build_resnet50_model():
    """
    Loads resnet model used for generating embeddings (bigger than the densenet models).
    Embeddings (out_vector of last fc layer is 1000 instead of 1024) are generated in second to last layer, after which the classifier (last layer of the nn) typically uses the embedding to produce its results.
    To access the embeddings without the classification, the named classifier-layer gets replaced with an identity layer to funnel through its input untouched.
    Additionally, the eval-flag prevents training and backpropagation.

    Returns:
        A resnet model without classifier that outputs embeddings of input images.
    """
    # load model via pytorch
    # resnet50 default weights are V2 with better performance
    model = models.resnet50(weights=ResNet50_Weights.DEFAULT)
    # replace classifier to access embeddings of preceeding layer (that would be the input for the classifier)
    model.classifier = nn.Identity()
    # user inference mode instead of training mode
    model.eval()
    return model
