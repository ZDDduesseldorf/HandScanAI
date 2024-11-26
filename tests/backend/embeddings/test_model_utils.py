import torch
from torchvision import models

from backend.embeddings import models_utils

### TESTS #############################################################


def test_densenet121():
    model = models_utils.load_model(models_utils.CNNModel.DENSENET_121)
    # expected is a model of type DenseNet
    assert type(model) is models.DenseNet
    # expected is that the last layer (classifier) was replaced by an identity-layer
    assert type(model.classifier) is torch.nn.Identity


def test_densenet169():
    model = models_utils.load_model(models_utils.CNNModel.DENSENET_169)
    # expected is a model of type DenseNet
    assert type(model) is models.DenseNet
    # expected is that the last layer (classifier) was replaced by an identity-layer
    assert type(model.classifier) is torch.nn.Identity


def test_restnet50():
    model = models_utils.load_model(models_utils.CNNModel.RESNET_50)
    # expected is a model of type ResNet
    assert type(model) is models.ResNet
    # expected is that the last layer (classifier) was replaced by an identity-layer
    assert type(model.classifier) is torch.nn.Identity
