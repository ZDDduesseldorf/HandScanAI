# Hand Normalization Pipeline

## How to Use

Before calculating the embedding, you must call the functions `segment_hand_image()` and `resize_images()` inside `hand_normalization/src/main.py`.  
- `segment_hand_image()` returns a list of slices of the main image in OpenCV format.  
- `resize_images()` transforms the images to the required sizes for the embedding network.


## What Happens Inside `segment_hand_image()`?

### 1. Creation of a Binary Mask

The mask is created using an HSV (Hue, Saturation, Value) approach. A region is defined that contains the range of valid skin tones. Everything outside this range is considered "not part of the hand." The resulting image looks like this:

![HandMask](https://github.com/user-attachments/assets/a7dad426-d855-4f5a-bde3-7bbf4d559afe)

### 2. Contour and Defect Detection

The hand mask is utilized to find the "outline" of the hand, called the contour.

![Contour](https://github.com/user-attachments/assets/6ecff463-964b-4cb5-aa4b-4354fb9b9c71)

To identify the spaces between the fingers, we use a concept called convexity defects.

![Defects Explained](https://github.com/user-attachments/assets/b4f10f3b-f54e-4c20-8f48-5049bc20d157)

By filtering all detected defects for the four with the largest defect distance (the distance between the point on the contour and the hull), we reliably find these points:

![Image with Defects](https://github.com/user-attachments/assets/e8831c57-e004-4dc9-8441-31fdf7fc22f7)

### 3. Defect Extrapolation through Line Casting

To identify the middle finger region, we connect the two defect points near the middle finger's base.  
With the current four points, we can only create regions for the middle and ring fingers. To extend this concept, we need to determine similar points for the other fingers. Our goal is to achieve something like this:

![Image with needed region defining points](https://github.com/user-attachments/assets/046c0f00-0563-4f39-8575-7643ed473052)

The points for the index and pinky fingers are determined by casting a line from the defect between the middle and ring fingers to the next defect point on either side. The points where these lines intersect the contour become the new region-defining points.  

The second region-defining point for the thumb is determined using the same principle, but with the **THUMB_MCP** point detected by Mediapipe's hand landmark model.  
The result looks like this:

![Image with all region defininf points](https://github.com/user-attachments/assets/06b3f430-4f09-44c2-917b-f5796824e015)

### 4. Separating the Regions

After connecting the regions on an image containing just the contour mask, the result looks like this:

![Contour_mask_region](https://github.com/user-attachments/assets/ceb95573-3c11-4924-8bd4-4a42c5b98d6c)

We then use a different contour detection method provided by OpenCV to extract contours within contours. These contours are converted into bitmasks and sorted by size, ensuring that the contour of the entire hand is always first:  

![Regions Bitmask Grid](https://github.com/user-attachments/assets/3a0b8b19-bc57-4d85-b68c-9af9d7c344dd)

To identify which mask corresponds to which region, we use landmarks from the Mediapipe model to check which regions contain which landmarks, and we assign each region accordingly.

### 5. Casting Bounding Boxes

To align the bounding box with the fingers and other segments, we rotate each region to point upwards. The angle of each region is calculated using two landmarks within the region.  

Next, the bounding boxes are calculated to fit the region bitmask with a 5-pixel boundary. A copy of the original image is rotated along with the region and then clipped to the bounding box. After resizing the images, the result looks like this:

![Regions Grid](https://github.com/user-attachments/assets/6eb9dcee-1430-4fcc-9152-5596b8229d73)
The order of the regions is as follows:  
**Hand, Hand Body, Thumb, Index Finger, Middle Finger, Ring Finger, Pinky Finger**.
