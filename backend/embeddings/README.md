# Embeddings module

- [Embeddings module](#embeddings-module)
  - [Contains](#contains)
  - [Currently implemented](#currently-implemented)
  - [Entry points](#entry-points)
    - [embeddings\_utils.py](#embeddings_utilspy)
    - [models\_utils.py](#models_utilspy)

## Contains

- **`embeddings_utils`**:
  - contains methods to calculate embeddings for images
- **`models_utils`**:
  - contains CNN-models for embeddings-calculation and transforms for image_preprocessing (before embeddings-calculation)

## Currently implemented

- Embeddings-calculation in backend via CNNs
- Models to choose from (implemented)
  - **DEFAULT: DenseNet (121, Acc@1 74, Acc@5 92, Params 8M (small))** -> Embeddings-Vector sized 1024
  - DenseNet (169, Acc@1 76, Acc@5 93, Params 14M (medium)) -> Embeddings-Vector sized 1664
  - ResNet (50|V2, Acc@1 81, Acc@5 95, Params 25.6M (medium/large)) -> Embeddings-Vector sized 1000
- Tests /tests/embeddings folder

Defaults are

- model = densenet121
- transforms = custom transforms (toImage, Resize, toFloat and rescale values between 0 and 1), see model_utils for further documentation.

## Entry points

### embeddings_utils.py

To calculate embeddings, use the suitable function from `embeddings_utils.py`. There are three options, depending on the format of the input images (a dict with image_path-values, a dict with numpy-array-values, a single 3-dimensional RGB Tensor (3, H, W)).

**The most common starting point is `calculate_embeddings_from_tensor_dict()` (used in pipelines, takes results from `hand_normalization`).**

You only need to specify the model if you want to use one of the alternatives, otherwise the default gets used (see [currently implemented](#currently-implemented)). For additional documentation, see the functions' respective doc strings.

### models_utils.py

All available models are loaded via pytorch. For additional documentation, see the respective doc strings.

**The most common starting point is `load_model()` (used in `embeddings_utils`).**
