# Embeddings module

## Table of contents

- [Embeddings module](#embeddings-module)
  - [Table of contents](#table-of-contents)
  - [Overview](#overview)
  - [Entry points](#entry-points)
    - [embeddings\_utils.py](#embeddings_utilspy)
    - [models\_utils.py](#models_utilspy)
  - [Currently implemented models](#currently-implemented-models)

## Overview

Embeddings are numerical representations of complex data that allow easier processing of that data (e.g. via machine learning).
In this application, we calculate embeddings of the normalized region images of a hand via a Convolutional Neural Network (CNN) and normalize them.

This module contains:

- **`embeddings_utils`**:
  - methods to calculate and normalize embeddings for images
- **`models_utils`**:
  - methods to load pytorch-CNN-models for embeddings-calculation and transforms for image_preprocessing (before embeddings-calculation)

The current defaults are

- **model** = densenet121
- **transforms** = custom transforms (toImage, Resize, toFloat and rescale values between 0 and 1), see model_utils for further documentation.
- **vector-norm** (for embeddings-normalization): L2

## Entry points

### embeddings_utils.py

To calculate embeddings, use the suitable function from `embeddings_utils.py`.

The most common starting point is `calculate_embeddings_from_tensor_dict()` (used in pipelines, takes results from `hand_normalization`).

It is one of three options, depending on the format of the input images (a dict with image_path-values, a dict with numpy-array-values, a single 3-dimensional RGB Tensor (3, H, W)). Generally, the module functions expect RGB color format.

You only need to specify the model if you want to use one of the alternatives, otherwise the default gets used (see [currently implemented models](#currently-implemented-models)). For additional documentation, see the functions' respective doc strings.

### models_utils.py

The most common starting point is `load_model()` (used in `embeddings_utils`).

All available models are loaded via pytorch. For additional documentation, see the respective doc strings.

## Currently implemented models

|Default|model name|embeddings vector length|pytorch metainformation|model size|
|---|---|---|---|---|
|**X**|**DenseNet121**|1024|Acc@1 74, Acc@5 92|Params 8M (small)|
| |DenseNet169|1664|Acc@1 76, Acc@5 93|Params 14M (medium)|
| |ResNet50, V2|1000|Acc@1 81, Acc@5 95|Params 25.6M (medium)|

DenseNet121 acts as default because it's the best compromise of the three in terms of speed, needed resources and accuracy (tested with the filtered 11K dataset via embeddings-scenario, see `tests/scenarios`). Might be updated in future versions after tests with different/ updated dataset.
