# imports

# image loading

# Mediapipe Landmarks
## <input> image array
## <output> landmarks array

# Defect Detection
## <input> image array
## apply gaussian filter
## create grayscale image + Multi-Otsu Thresholding
## skeletonize image
## calculate Center of Mass
## calculate pinky defect
## <output> ...

# Segmentation
## <input> ?
## palm mask
## finger mask
## isolate finger mask into multiple masks
## crop segment masks
## <output> ...

# Rotate segments
## <input> landmarks array 
## calculate rotation
## apply rotation
## <output> ...

# Resize segments
## 