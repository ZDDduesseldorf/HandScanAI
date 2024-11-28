import functions
import cv2
import numpy as np

def segment_hand_image(image_path):
    # image loading
    original_image = cv2.imread(image_path) # -> Abhängig von Bilderübergabe Frontend
    grey_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    # Create placeholder image
    image_height, image_width = grey_image.shape
    blank_image = np.zeros((image_height, image_width), dtype=np.uint8)

    # Mediapipe Landmarks
    landmarks = functions.getLandmarks(image_path) # -> Abstimmung Frontend, um Redundanz zu vermeiden

    # Create a mask for the skin color
    hand_mask = functions.create_handmask(original_image)

    # find contour and defects
    contours, _ = cv2.findContours(hand_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Find the largest contour by area
        largest_contour = max(contours, key=cv2.contourArea)

        # Draw the largest contour on a Contour image
        contour_mask = blank_image.copy()
        cv2.drawContours(contour_mask, [largest_contour], -1, 255, 2) 
                
        four_largest_defects = functions.detect_largest_defects(largest_contour)
    
    # Define lookup areas for defect identification 
    lookup_area_middle_ring_defect = np.array([landmarks[9],landmarks[10],landmarks[14],landmarks[13]])
    lookup_area_pinkie_ring_defect = np.array([landmarks[13],landmarks[14],landmarks[18],landmarks[17]])
    lookup_area_middle_index_defect = np.array([landmarks[5],landmarks[6],landmarks[10],landmarks[9]])
    lookup_area_inner_thumb_defect = np.array([landmarks[5],landmarks[1],landmarks[2],landmarks[3]])
    
    lookup_areas = [
        lookup_area_inner_thumb_defect,
        lookup_area_middle_index_defect,  
        lookup_area_middle_ring_defect,
        lookup_area_pinkie_ring_defect
        ]

    # Identify defects by determined lookup areas
    specified_defects = []
    for area in lookup_areas:
        lookup_area_mask = functions.hull_or_contour_to_bitmask(area, grey_image.shape)
        specified_defects.append(functions.check_points_in_mask(lookup_area_mask,four_largest_defects)[0])

    # Find intersection points with hand contour by casting lines to detect missing defects
    outer_thumb_defect = functions.detect_missing_point(specified_defects[0], landmarks[2], contour_mask, blank_image)
    index_defect = functions.detect_missing_point(specified_defects[2], specified_defects[1], contour_mask, blank_image)
    pinkie_defect = functions.detect_missing_point(specified_defects[2], specified_defects[3], contour_mask, blank_image)

    specified_defects.insert(0, outer_thumb_defect)
    specified_defects.insert(2, index_defect)
    specified_defects.append(pinkie_defect)

    segmented_contour_mask = contour_mask.copy()

    # Draw segment lines between hand defects on hand contour
    for idx, _ in enumerate(specified_defects):
        if idx != 1 and idx != 6:
            cv2.line(segmented_contour_mask, specified_defects[idx], specified_defects[idx+1], 255, 2)

    # Find contours and inner contours
    hand_segment_contours, _ = cv2.findContours(segmented_contour_mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create bitmasks for each region
    hand_segments = []
    for contour in hand_segment_contours:
        segment_bitmask = functions.hull_or_contour_to_bitmask(contour,blank_image.shape)
        hand_segments.append(segment_bitmask)

    # Extraction
    ## <input> hand_segments bitmasks

    # Detect hand orientation (thumb on left or right side)
    ring_finger_base = landmarks[13]
    index_finger_base = landmarks[5]
    if ring_finger_base[0] > index_finger_base[0]: 
        orientation_hand = -1
    else:
        orientation_hand = 1
    
    ## "reference_point" marks a landmark that must be contained inside of the segment
    ## "angle" is the angle the image needs to be rotadet to be oriented from bottom to top
    regions = [
    {
        "name": "Hand",
        "reference_point": [],
        ## the refence points that calculate the angle of hand and palm are shifted by -90°  
        "angle": 90 -  orientation_hand *  functions.vector_agle(landmarks[5], landmarks[13]),
    },
    {
        "name": "Palm",
        "reference_point": landmarks[13],
        "angle": 90 - orientation_hand * functions.vector_agle(landmarks[5], landmarks[13]),
    },
    {
        "name": "Thumb",
        "reference_point": landmarks[3],
        "angle": 180 - functions.vector_agle(landmarks[2], landmarks[4]),
    },
    {
        "name": "Index Finger",
        "reference_point": landmarks[7],
        "angle": 180 - functions.vector_agle(landmarks[6], landmarks[8]),
    },
    {
        "name": "Middle Finger",
        "reference_point": landmarks[11],
        "angle": 180 - functions.vector_agle(landmarks[10], landmarks[12]),
    },
    {
        "name": "Ring Finger",
        "reference_point": landmarks[15],
        "angle": 180 - functions.vector_agle(landmarks[14], landmarks[16]),
    },
    {
        "name": "Pinky Finger",
        "reference_point": landmarks[19],
        "angle": 180 - functions.vector_agle(landmarks[18], landmarks[20]),
    },
]

    # Assign hand segement mask to correct region
    regions[0].update({"mask": hand_segments[0]}) # Whole hand image has to be assigned seperatly due to missing reference point
    for region in regions[1:]:
        region_reference_point = region["reference_point"]
        for segments in hand_segments[1:]:
            points_in_segment = functions.check_points_in_mask(segments,region_reference_point)
            if(points_in_segment):
                region.update({"mask": segments}) 

    for region in regions:
        image = original_image.copy()
        ## rotate clean and segmented image
        image_rotated = functions.rotate_image_no_crop(image, region["angle"])
        segment_mask_rotaded = functions.rotate_image_no_crop(region["mask"], region["angle"])
        ## calculate boundingbox of the mask
        bounding_box = functions.get_bounding_box_with_margin(segment_mask_rotaded, 5)
        ## crop original image to bounding box
        cropped_segment_image = functions.crop_to_bounding_box(image_rotated, bounding_box)
        ## write the cropped image and the segment mask to regions dict 
        region.update({"segment_image": cropped_segment_image}) 

    ##  write the images in the dict to the output list to preserve a constant segment ordering in the list
    images = []
    for region in regions:
        images.append(region["segment_image"])
    return images

## dynamic segment sizing
def resize_images(images, size = 224, fill_color=(255, 255, 255)):
    resized_regions = []
    for region in images:
        resized_region = functions.dynamic_resize_image_to_target(region, size, fill_color)
        resized_regions.append(resized_region)
    
    return resized_regions

# images = segment_hand_image("C:\\Users\lukas\Documents\Local-Repositories\HandScanAI\hand_normalization\TestImages\Hand_0000064.jpg")
# images = resize_images(images)
# functions.show_images(images)

# images = segment_hand_image("J:\VSCODE\HandScanAI-1\hand_normalization\TestImages\Hand_0000523.jpg")
# images = resize_images(images)
# functions.show_images(images)

# images = segment_hand_image("J:\VSCODE\HandScanAI-1\hand_normalization\TestImages\Hand_0000064.jpg")
# images = resize_images(images)
# functions.show_images(images)

# images = segment_hand_image("J:\VSCODE\HandScanAI-1\hand_normalization\TestImages\Hand_0000455.jpg")
# images = resize_images(images)
# functions.show_images(images)