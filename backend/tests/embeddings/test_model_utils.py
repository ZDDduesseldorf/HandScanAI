import torch
from torchvision import models

from backend.embeddings import models_utils

### TESTS #############################################################


def test_densenet121():
    model = models_utils.load_model(models_utils.CNNModel.DENSENET_121)
    # expected is a model of type DenseNet
    if type(model) is not models.DenseNet:
        raise AssertionError("Expected model to be of type DenseNet")
    # expected is that the last layer (classifier) was replaced by an identity-layer
    if type(model.classifier) is not torch.nn.Identity:
        raise AssertionError("Expected classifier to be of type Identity")


def test_densenet169():
    model = models_utils.load_model(models_utils.CNNModel.DENSENET_169)
    # expected is a model of type DenseNet
    if type(model) is not models.DenseNet:
        raise AssertionError("Expected model to be of type DenseNet")
    # expected is that the last layer (classifier) was replaced by an identity-layer
    if type(model.classifier) is not torch.nn.Identity:
        raise AssertionError("Expected classifier to be of type Identity")


def test_restnet50():
    model = models_utils.load_model(models_utils.CNNModel.RESNET_50)
    # expected is a model of type ResNet
    if type(model) is not models.ResNet:
        raise AssertionError("Expected model to be of type ResNet")
    # expected is that the last layer (classifier) was replaced by an identity-layer
    if type(model.classifier) is not torch.nn.Identity:
        raise AssertionError("Expected classifier to be of type Identity")
