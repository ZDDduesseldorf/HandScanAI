# imports
import functions
import cv2
import numpy as np
from skimage.morphology import skeletonize
from skimage.filters import threshold_multiotsu

def normalize_hand_image(image_path):
    # image loading
    original_image = cv2.imread(image_path)
    clean_image = cv2.imread(image_path)
    grey_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    # Mediapipe Landmarks
    ## <input> image array
    ## <output> landmarks array
    landmarks = functions.getLandmarks(image_path)
    # landmark display
    for landmark in landmarks:
        cv2.circle(original_image, (landmark[1],landmark[2]), radius=3, color=(0, 0,0), thickness=4)

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
        # Draw the largest contour on a Contour image
        image_height, image_width = grey_image.shape
        blank_image = np.zeros((image_height, image_width), dtype=np.uint8)
        contour_mask = blank_image.copy()
        cv2.drawContours(contour_mask, [largest_contour], -1, 255, 2) 

        
        defect_distances = []
        for i in range(defects.shape[0]):
            # Extract defect details
            start_idx, end_idx, farthest_idx, defect_distance = defects[i, 0]
            farthest_point = tuple(largest_contour[farthest_idx][0])

            
            defect_distances.append([defect_distance,farthest_point])

        defect_distances.sort(reverse=True)
        four_largest_defects = []
        for i in range(4):
           four_largest_defects.append(defect_distances[i][1])
           cv2.circle(image_with_defects, defect_distances[i][1], radius=3, color=(0, 0, 255), thickness=5)
    
    ## find Rotation and Roteat Image 
    # hand_orientation_vector = (landmarks[5][1] - landmarks[17][1] , landmarks[5][2] - landmarks[17][2])
    # hand_angle = cv2.fastAtan2(hand_orientation_vector[0],hand_orientation_vector[1]) + 90
    
    # rotated_image = functions.rotate_image_no_crop(original_image, -hand_angle)
 

    ## cleanup hand mask
    clean_hand_mask = functions.hull_or_contour_to_bitmask(largest_contour, grey_image.shape)

    ## find contours
    # Find all contours in the binary mask

    ## calculate pinky and Index defect
    
    ### find defect between middle and ring finger
    #### create the mask of the area defined by landmark points
    lookup_area_middle_ring_defect = np.array([landmarks[9][1:],landmarks[10][1:],landmarks[14][1:],landmarks[13][1:]])
    lookup_area_middle_ring_mask = functions.hull_or_contour_to_bitmask(lookup_area_middle_ring_defect, grey_image.shape)
    #### check wich defects are insed the mask
    middle_ring_defect = functions.check_points_in_mask(lookup_area_middle_ring_mask,four_largest_defects)[0]

    #### repeat for Pinkie_ring_finger defect
    lookup_area_pinkie_ring_defect = np.array([landmarks[13][1:],landmarks[14][1:],landmarks[18][1:],landmarks[17][1:]])
    lookup_area_pinkie_ring_mask = functions.hull_or_contour_to_bitmask(lookup_area_pinkie_ring_defect, grey_image.shape)
    pinkie_ring_defect = functions.check_points_in_mask(lookup_area_pinkie_ring_mask,four_largest_defects)[0]

    #### cast a line from the middle_ring defect towards the pinkie_ring defect and look for intersection points with the contour of the hand. The Outer most point is our constructed pinkie finger defect 
    direction_vector_to_pinkie_defect = functions.direction_vector(middle_ring_defect,pinkie_ring_defect)
    moved_point = (int(middle_ring_defect[0] + direction_vector_to_pinkie_defect[0] * 3), int(middle_ring_defect[1] + direction_vector_to_pinkie_defect[1] * 3))
    line_mask = blank_image.copy()
    line_mask = cv2.line(line_mask, middle_ring_defect, moved_point, 255, 1)

    # Find the intersection by using bitwise AND
    intersections = cv2.bitwise_and(contour_mask, line_mask)

    # Find coordinates of the intersection points
    swapped_intersection_points = np.column_stack(np.where(intersections == 255))
    ### swap point to back cv2 style 
    intersection_points = [(x, y) for y, x in swapped_intersection_points]
    for point in intersection_points:
        cv2.circle(original_image,point, radius=3, color=(0, 0, 255), thickness=5)

    # Find the closest intersection point to the moved point
    pinkie_defect = functions.find_closest_point(intersection_points, moved_point)
    cv2.circle(image_with_defects, pinkie_defect, radius=3, color=(0, 0, 255), thickness=5)

    ### repeat for index finger defect
    #### repeat for pinkie_ring_finger defect
    lookup_area_middle_index_defect = np.array([landmarks[5][1:],landmarks[6][1:],landmarks[10][1:],landmarks[9][1:]])
    lookup_area_middle_index_mask = functions.hull_or_contour_to_bitmask(lookup_area_middle_index_defect, grey_image.shape)
    middle_index_defect = functions.check_points_in_mask(lookup_area_middle_index_mask,four_largest_defects)[0]

    #### cast line 
    direction_vector_to_index_defect = functions.direction_vector(middle_ring_defect,middle_index_defect)
    moved_point = (int(middle_ring_defect[0] + direction_vector_to_index_defect[0] * 3), int(middle_ring_defect[1] + direction_vector_to_index_defect[1] * 3))
    line_mask = blank_image.copy()
    line_mask = cv2.line(line_mask, middle_ring_defect, moved_point, 255, 1)

    # Find the intersection by using bitwise AND
    intersections = cv2.bitwise_and(contour_mask, line_mask)

    # Find coordinates of the intersection points
    swapped_intersection_points = np.column_stack(np.where(intersections == 255))
    ### swap point to back cv2 style 
    intersection_points = [(x, y) for y, x in swapped_intersection_points]
    for point in intersection_points:
        cv2.circle(original_image,point, radius=3, color=(0, 0, 255), thickness=5)

    # Find the closest intersection point to the moved point
    index_defect = functions.find_closest_point(intersection_points, moved_point)
    cv2.circle(image_with_defects, index_defect, radius=3, color=(0, 0, 255), thickness=5)

    ### repeat for Outer Thumb defect but whith Inner Thumb defect and a Thumb Landmark
    lookup_area_inner_thumb_defect = np.array([landmarks[5][1:],landmarks[1][1:],landmarks[2][1:],landmarks[3][1:]])
    lookup_area_inner_thumb_mask = functions.hull_or_contour_to_bitmask(lookup_area_inner_thumb_defect, grey_image.shape)
    inner_thumb_defect = functions.check_points_in_mask(lookup_area_inner_thumb_mask,four_largest_defects)[0]

    #### cast line 
    direction_vector_to_outer_thumb_defect = functions.direction_vector(inner_thumb_defect,landmarks[2][1:])
    moved_point = (int(inner_thumb_defect[0] + direction_vector_to_outer_thumb_defect[0] * 3), int(inner_thumb_defect[1] + direction_vector_to_outer_thumb_defect[1] * 3))
    line_mask = blank_image.copy()
    line_mask = cv2.line(line_mask, inner_thumb_defect, moved_point, 255, 1)

    # Find the intersection by using bitwise AND
    intersections = cv2.bitwise_and(contour_mask, line_mask)

    # Find coordinates of the intersection points
    swapped_intersection_points = np.column_stack(np.where(intersections == 255))
    ### swap point to back cv2 style 
    intersection_points = [(x, y) for y, x in swapped_intersection_points]
    for point in intersection_points:
        cv2.circle(original_image,point, radius=3, color=(0, 0, 255), thickness=5)

    # Find the closest intersection point to the moved point
    outer_thumb_defect = functions.find_closest_point(intersection_points, moved_point)
    cv2.circle(image_with_defects, outer_thumb_defect, radius=3, color=(0, 0, 255), thickness=5)
    ## <output> ...

    # Segmentation
    ## <input> contour_mask
    ## copy hand contour
    segmented_contour_mask = contour_mask.copy()
    ## draw segment lines between hand defects on hand contour
    cv2.line(segmented_contour_mask, pinkie_defect, pinkie_ring_defect, 255, 2)
    cv2.line(segmented_contour_mask, pinkie_ring_defect, middle_ring_defect, 255, 2)
    cv2.line(segmented_contour_mask, middle_ring_defect, middle_index_defect, 255, 2)
    cv2.line(segmented_contour_mask, middle_index_defect, index_defect, 255, 2)
    cv2.line(segmented_contour_mask, inner_thumb_defect, outer_thumb_defect, 255, 2)

    ## find contours and inner contours
    hand_segment_contours, _ = cv2.findContours(segmented_contour_mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    
    ## create bitmasks for each region
    hand_segments = []
    for contour in hand_segment_contours:
        segment_bitmask = functions.hull_or_contour_to_bitmask(contour,blank_image.shape)
        hand_segments.append(segment_bitmask)
    ## <output> ...

    ## set bonding boxes for segments
    ## loop over segments
    ##      rotate segment and image to segment orientation
    ##      set boundingbox around segment
    ##      crop original image at boundingbox
    ## return the segments
    regions = [
    {
        "name": "Hand",
        "reference_point": [],
        "angle": 180-functions.vector_agle(landmarks[5][1:], landmarks[13][1:])-90,
    },
    {
        "name": "Palm",
        "reference_point": landmarks[13][1:],
        "angle": 180-functions.vector_agle(landmarks[5][1:], landmarks[13][1:])-90,
    },
    {
        "name": "Thumb",
        "reference_point": landmarks[3][1:],
        "angle": 180-functions.vector_agle(landmarks[2][1:], landmarks[4][1:]),
    },
    {
        "name": "Index Finger",
        "reference_point": landmarks[7][1:],
        "angle": 180-functions.vector_agle(landmarks[6][1:], landmarks[8][1:]),
    },
    {
        "name": "Middle Finger",
        "reference_point": landmarks[11][1:],
        "angle": 180-functions.vector_agle(landmarks[10][1:], landmarks[12][1:]),
    },
    {
        "name": "Ring Finger",
        "reference_point": landmarks[15][1:],
        "angle": 180-functions.vector_agle(landmarks[14][1:], landmarks[16][1:]),
    },
    {
        "name": "Pinky Finger",
        "reference_point": landmarks[19][1:],
        "angle": 180-functions.vector_agle(landmarks[18][1:], landmarks[20][1:]),
    },
]
    
    
    image = clean_image.copy()
    image_rotaded = functions.rotate_image_no_crop(image, regions[0]["angle"])
    segment_mask_rotaded = functions.rotate_image_no_crop(hand_segments[0], regions[0]["angle"])
    bounding_box = functions.get_bounding_box_with_margin(segment_mask_rotaded, 5)
    cropped_segment_image = functions.crop_to_bounding_box(image_rotaded, bounding_box)
    regions[0].update({"mask": hand_segments[0]}) 
    regions[0].update({"segment_image": cropped_segment_image}) 

    for region in regions[1:]:
        region_reference_point = region["reference_point"]
        for segments in hand_segments[1:]:
            points_in_segment = functions.check_points_in_mask(segments,region_reference_point)
            if(points_in_segment):
                image = clean_image.copy()
                print(f"rotated " + region["name"] + " by: " + str(region["angle"]))
                image_rotaded = functions.rotate_image_no_crop(image, region["angle"])
                segment_mask_rotaded = functions.rotate_image_no_crop(segments, region["angle"])
                bounding_box = functions.get_bounding_box_with_margin(segment_mask_rotaded, 5)
                cropped_segment_image = functions.crop_to_bounding_box(image_rotaded, bounding_box)
                region.update({"mask": segments}) 
                region.update({"segment_image": cropped_segment_image}) 

    images = []
    for region in regions:
        images.append(region["segment_image"])
    return images

## dynamic segment sizing
## loop over segments
##      resize segment to 224x224
##      fill rest of 224x224 with 0 or 255,255,255?
## returns embedding ready segments

## static segment sizing
## loop over segments
##      resize segment to with a static segment scaling
##      fill rest of 224x224 with 0 or 255,255,255?
## returns embedding ready segments

images = normalize_hand_image("C:\\Users\lukas\Documents\Local-Repositories\HandScanAI\hand_normalization\TestImages\Hand_0000064.jpg")
for image in images:
    cv2.imshow("hand region multi otsu",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

fill_color=(0, 0, 0)
size = 224

for region in images:
    resized_region = functions.dynamic_resize_image_to_target(region, size, fill_color)
    cv2.imshow("check", resized_region)
    cv2.waitKey(0)
    cv2.destroyAllWindows