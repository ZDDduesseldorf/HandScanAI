# README

## TODO

- test and update embedding calculation with results of hand normalization
- integrate embeddings into backend

## Current branch

### Create an environment

In the folder with the `environment.yml` file, run:

```
conda update -n base -c defaults conda  # optional (to make sure conda is up to date)
conda env create -f environment.yml
```

This should create a Python 3.10 environment with the packages listed in the yaml-file.

### Update the environment

If new dependency is required,

- add it in `environment.yml`,
- activate environment
- run the following (prune deinstalls deleted dependencies):
```conda env update --file environment.yml --prune```

### Current Status

- embedding-calculation in seperate module (see backend TODO)
- load pictures automatically with path (see hand-normalization TODO)
- models used/ implemented
  - **DenseNet (121, Acc@1 74, Acc@5 92, Params 8M (small))** -> Embeddings-Size 1024
  - **ResNet (50|V2, Acc@1 81, Acc@5 95, Params 25.6M (medium/large))** -> Embeddings-Size 1000
