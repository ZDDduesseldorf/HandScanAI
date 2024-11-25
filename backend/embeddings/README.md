# README

## TODO

- test and update embedding calculation with results of hand normalization

## Current branch

### Current Status

- embedding-calculation in backend
- load pictures automatically with path (see hand-normalization TODO)
- models used/ implemented
  - **DenseNet (121, Acc@1 74, Acc@5 92, Params 8M (small))** -> Embeddings-Size 1024
  - **ResNet (50|V2, Acc@1 81, Acc@5 95, Params 25.6M (medium/large))** -> Embeddings-Size 1000
