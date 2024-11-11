# imports
import functions
import cv2
import numpy as np
from skimage.morphology import skeletonize
from skimage.filters import threshold_multiotsu

def normalize_hand_image(image_path):
    # image loading
    original_image = cv2.imread(image_path)
    grey_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    # Mediapipe Landmarks
    ## <input> image array
    ## <output> landmarks array
    landmarks = functions.getLandmarks(image_path)

    # Defect Detection
    ## <input> image array
    ## apply gaussian filter
    blurred_image = cv2.GaussianBlur(original_image, (11, 11), 2)


    # Define the range for skin color in HSV(Hue, Saturation, Value)
    # These values might need to be adjusted depending on lighting and skin tone
    hsv = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2HSV)

    lower_skin = np.array([0, 40, 80])  # Lower bound of skin color (Hue, Saturation, Value)
    upper_skin = np.array([20, 255, 255])  # Upper bound of skin color

    # Create a mask for the skin color
    hand_mask = cv2.inRange(hsv, lower_skin, upper_skin)
    # Apply the mask to the original image to get the segmented hand
    # segmented_hand = cv2.bitwise_and(blurred_image, blurred_image, mask=skin_mask)

    # find contour and defects
    contours, _ = cv2.findContours(hand_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Find the largest contour by area
        largest_contour = max(contours, key=cv2.contourArea)

        # Find the convex hull of the largest contour
        hull = cv2.convexHull(largest_contour, returnPoints=False)

        # Find the convexity defects
        defects = cv2.convexityDefects(largest_contour, hull)

        # Draw the largest contour on the original image
        image_with_defects = original_image.copy()
        cv2.drawContours(image_with_defects, [largest_contour], -1, (0, 255, 0), 2) 
    
 

    ## skeletonize image
    clean_hand_mask = functions.hull_or_contour_to_bitmask(largest_contour, grey_image.shape)
    hand_skeleton = skeletonize(clean_hand_mask.astype(np.uint8) * 255)

    skeleton_mask =  hand_skeleton* clean_hand_mask

    return skeleton_mask, clean_hand_mask
    # return skeleton_mask
    ## calculate Center of Mass
    inverted_hand_region = 255 - hand_region
    hand_skeleton = skeletonize(inverted_hand_region)
    hand_skeleton_uint8 = (hand_skeleton * 255).astype(np.uint8)
    center_of_mass = functions.calculate_center_of_mass(hand_skeleton_uint8)
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

# images = normalize_hand_image("J:\VSCODE\HandScanAI-1\hand_normalization\TestImages\Hand_0000658.jpg")
# for image in images:
#     cv2.imshow("hand region multi otsu",image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()