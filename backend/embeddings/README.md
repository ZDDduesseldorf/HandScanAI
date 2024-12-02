# README

## TODO

- test and update embedding calculation with results of hand normalization

## Current branch

### Current Status

- embedding-calculation in backend
- tests in sibling /tests folder
- load pictures automatically with path (see hand-normalization TODO)
- models used/ implemented
  - **DEFAULT: DenseNet (121, Acc@1 74, Acc@5 92, Params 8M (small))** -> Embeddings-Size 1024
  - DenseNet (169, Acc@1 76, Acc@5 93, Params 14M (medium)) -> Embeddings-Size 1024
  - ResNet (50|V2, Acc@1 81, Acc@5 95, Params 25.6M (medium/large)) -> Embeddings-Size 1000

Defaults are

- model = densenet121
- transforms = custom transforms (toImage, Resize, toFloat and rescale values between 0 and 1), see model_utils for further information.

### Entry point

To calculate embeddings, use the suitable function from `embeddings_utils.py`. There are three options, depending on the format of the input images (one image, multiple images, image paths).

You only need to specify the model if you want to use one of the alternatives, but not if you want to use the default.

All available models are loaded via pytorch. For additional documentation, see the respective doc strings.
