from validation.validation_pipeline import validation_pipeline, is_validation_pipeline_valid

### This pipeline is for filtering 11K dataset

# TODO: load images from 11K Dataset
# dataloader

# TODO: Validate/ filter images
# use validation pipeline (see websocket)
# save validated images in folder and metadata in csv
# image path: UUID.pdf (see websocket)
# result: base dataset

# TODO: hand-normalization
# dataloader
# save normalized images (path: UUID_HandRegion)
# provide Hand-regions as Enum or something similar to standardize path reading

# TODO: embeddings
# dataloader (loading with path)
# calculate embeddings
# provide embeddings per region to

# TODO: kNN (vector tree)
# one kNN Tree per Hand-region
# save models/trees (lokal folder/ teams?)
