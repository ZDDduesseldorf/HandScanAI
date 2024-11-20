import numpy as np

def spread_check(landmarks, general_threshold=50, thumb_index_threshold=100):
    #define indices of finger joints 
    #source: mediapipe api docs:
    #https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer
    finger_indices = {
        "thumb": 3,
        "index": 6,
        "middle": 10,
        "ring": 14,
        "pinky": 18,
    }

    if landmarks:

        #get coordinates for each finger joint
        fingers = {name: landmarks[idx] for name, idx in finger_indices.items()}

        #define the order of adjacent fingers
        adjacent_fingers = ["thumb", "index", "middle", "ring", "pinky"]

        #calculate distance of adjacent fingers 
        #adjacent fingers are relevant for measuring spread
        adjacent_distances = {}
        for i in range(len(adjacent_fingers) - 1):
            finger1 = adjacent_fingers[i]
            finger2 = adjacent_fingers[i + 1]
            
            coord1 = fingers[finger1]
            coord2 = fingers[finger2]
            
            #calculate euclidian distance (in pixels)
            distance = np.linalg.norm(np.array(coord1) - np.array(coord2))
            adjacent_distances[(finger1, finger2)] = distance

        #for now just print the distance to the console
        for finger_pair, distance in adjacent_distances.items():
            #print(f"Distance between {finger_pair[0]} and {finger_pair[1]}: {distance:.2f} pixels")
            #todo: define threshold and return boolean if spread is ok
            if finger_pair == ("thumb", "index"):  # Apply thumb-index specific threshold
                print(f"Distance between {finger_pair[0]} and {finger_pair[1]}: {distance:.2f} pixels")
                if distance < thumb_index_threshold:
                    return False
            else:  # Apply general threshold for other pairs
                print(f"Distance between {finger_pair[0]} and {finger_pair[1]}: {distance:.2f} pixels")
                if distance < general_threshold:
                    return False

        return True  # Spread is okay
    else:
        return False