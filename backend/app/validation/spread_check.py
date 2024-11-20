import numpy as np

def spread_check(landmarks, thresholds={"thumb-index":1.5, "pinky-ring":0.55, "rest": 0.6}):
    """
    Check the spread of the fingers

    :param landmarks: List of landmarks of the hand
    :param thresholds: Dictionary with thresholds for specific pairs and the rest of the fingers.
    :return Boolean: Returns true, if the all fingers are spreaded above the specified (or default) threshold
    """

    #define indices of finger joints 
    #source: mediapipe api docs:
    #https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer

    # Define indices of PIP and MCP joints for each finger
    # The thumb does not have a PIP, so IP is used.
    # PIP = Proximal interphalangeal (middle joint)
    # MCP = Metacarpophalangeal (base joint)
    pip_indices = {
        "thumb": 3, #this is IP not PIP
        "index": 6,
        "middle": 10,
        "ring": 14,
        "pinky": 18,
    }
    mcp_indices = {
        "thumb": 2,
        "index": 5,
        "middle": 9,
        "ring": 13,
        "pinky": 17,
    }

    if landmarks:

        #get coordinates for each finger joint
        fingers = {name: landmarks[idx] for name, idx in pip_indices.items()}

        # calculate PIP-MCP distances for each finger
        pip_mcp_distances = {
            name: np.linalg.norm(np.array(landmarks[pip_idx]) - np.array(landmarks[mcp_indices[name]]))
            for name, pip_idx in pip_indices.items()
        }

        # calculate relative distances and check thresholds
        relative_distances, is_valid = calculate_relative_distances_pip_mcp(
            fingers, pip_mcp_distances, thresholds
        )

        # display results for check
        for finger_pair, rel_distance in relative_distances.items():
            print(
                f"Relative distance between {finger_pair[0]} and {finger_pair[1]}: {rel_distance:.2f}"
            )

        return is_valid
    else:
        print("No hand landmarks provided.")
        return False


def calculate_relative_distances_pip_mcp(fingers, pip_mcp_distances, thresholds):
    """
    Calculate relative distances between adjacent fingers normalized by PIP-MCP distances.

    :param fingers: Dictionary of fingertip coordinates.
    :param pip_mcp_distances: Dictionary of PIP-MCP distances for each finger.
    :param thresholds: Dictionary with thresholds for specific pairs and the rest.
    :return: Tuple (relative_distances, result), where:
             - relative_distances: Dictionary of relative distances between adjacent fingertips.
             - result: Boolean indicating if all distances meet their thresholds.
    """
    adjacent_fingers = ["thumb", "index", "middle", "ring", "pinky"]
    relative_distances = {}
    is_valid = True

    # do all steps for all adjacent finger pairs
    for i in range(len(adjacent_fingers) - 1):
        finger1 = adjacent_fingers[i]
        finger2 = adjacent_fingers[i + 1]
        
        # get joint coordinates
        coord1 = fingers[finger1]
        coord2 = fingers[finger2]

        # calculate joint distance
        fingerjoint_distance = np.linalg.norm(np.array(coord1) - np.array(coord2))

        # use the average PIP-MCP distance for normalization
        avg_pip_mcp_distance = (pip_mcp_distances[finger1] + pip_mcp_distances[finger2]) / 2

        # avoid division by zero
        if avg_pip_mcp_distance == 0:
            relative_distance = float('inf')  # Handle degenerate case
        else:
            relative_distance = fingerjoint_distance / avg_pip_mcp_distance

        # store the relative distance
        relative_distances[(finger1, finger2)] = relative_distance

        # determine the threshold for this pair
        if (finger1, finger2) == ("thumb", "index"):
            threshold = thresholds["thumb-index"]
        elif (finger1, finger2) == ("pinky", "ring"):
            threshold = thresholds["pinky-ring"]
        else:
            threshold = thresholds["rest"]

        # check against the threshold
        if relative_distance < threshold:
            is_valid = False

    return relative_distances, is_valid