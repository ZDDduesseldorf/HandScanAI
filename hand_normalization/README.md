# Hand Normalization Pipline

## How to Use
To use the code before the embedding calculation the functions 'segment_hand_image()' und 'resize_images()' inside hand_normilization/src/main.py must be called. 'segment_hand_image()' returns a list of slices of the main image in an open cv format.
'resize_images()' can then be used to transform the images to the needed sizes for the embedding network.

## What Happens Inside 'segment_hand_image()'?

### 1. Creation of a Binary Mask

The mask is created using a HSV (Hue, Saturation, Value) approach. A Region is defined that contains the range of valid skin tones. Everything outside this range is regarded as "not part of Hand". The resulting Image looks something like this:

![HandMask](https://github.com/user-attachments/assets/a7dad426-d855-4f5a-bde3-7bbf4d559afe)

### 2. Contour and Defect Detection

Now the hand mask ist utilized to find the "outline" of the hand this is called the contour.

![Contour](https://github.com/user-attachments/assets/6ecff463-964b-4cb5-aa4b-4354fb9b9c71)

To identify the spots between the fingers we use a conept called convexity defects. ![image](https://github.com/user-attachments/assets/b4f10f3b-f54e-4c20-8f48-5049bc20d157)
This provides us with 4 usable points. These are the ones which have the four largest convexity defect distances reliably:

![Image with Defects](https://github.com/user-attachments/assets/e8831c57-e004-4dc9-8441-31fdf7fc22f7)

### 3. Defect Extrapolation through Lincasting

Utilizing the found defcets we can use them to find even more points by which we can devide the hand. Our goal is something like this:

![Image with needed points](https://github.com/user-attachments/assets/046c0f00-0563-4f39-8575-7643ed473052)

We find these point by casting a line between 


### 4. Connecting the Defects
### 5. Contour and Subcontour Detection
### 6. Segment Rotation
### 7. Casting Boundingboxes
