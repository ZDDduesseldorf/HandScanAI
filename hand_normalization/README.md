# Hand Normalization Pipline

## How to Use
To use the code before the embedding calculation the functions 'segment_hand_image()' und 'resize_images()' inside hand_normilization/src/main.py must be called. 'segment_hand_image()' returns a list of slices of the main image in an open cv format.
'resize_images()' can then be used to transform the images to the needed sizes for the embedding network.

## What Happens Inside 'segment_hand_image()'?


