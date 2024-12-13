import numpy as np


def hand_is_spread(landmarks, thresholds=None, debug=False):
    """
    Check if the fingers are sufficiently spread.

    :param landmarks: List of landmarks of the hand (as returned by MediaPipe or similar library).
    :param thresholds: Dictionary with thresholds for specific finger pairs and the rest of the fingers.
                       Default values are provided for "thumb-index", "pinky-ring", and "rest".
    :param debug: If set to True, logs are printed to the console for debugging. Default is False.
    :return: True if all fingers meet their specified or default threshold, False otherwise.
    """
    if(thresholds is None):
        thresholds = {"thumb-index": 1.15, "pinky-ring": 1.35, "rest": 1.10}

    if thresholds is None:
        thresholds = {"thumb-index": 1.20, "pinky-ring": 1.40, "rest": 1.15}

    # Define indices for PIP (proximal interphalangeal) and MCP (metacarpophalangeal) joints
    # Note: The thumb does not have a PIP joint; its IP (interphalangeal) joint is used instead.
    # Source: Mediapipe API docs: https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer
    pip_indices = {
        "thumb": 3,  # this is the IP joint, not PIP
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

    # ensure landmarks are provided
    if landmarks:
        # get PIP and MCP coordinates for each joint
        pip_coords = {name: landmarks[idx] for name, idx in pip_indices.items()}
        mcp_coords = {name: landmarks[idx] for name, idx in mcp_indices.items()}

        # calculate relative distances and check thresholds
        relative_distances, is_valid = calculate_relative_distances_pip_mcp(pip_coords, mcp_coords, thresholds)

        # log results if debug is enabled
        if debug:
            for finger_pair, rel_distance in relative_distances.items():
                print(f"Relative distance between {finger_pair[0]} and {finger_pair[1]}: {rel_distance:.2f}")

        return is_valid
    else:
        if debug:
            print("No hand landmarks provided.")
        return False


def calculate_relative_distances_pip_mcp(pip_indices, mcp_indices, thresholds):
    """
    Calculate relative distances between adjacent fingers, normalized by MCP distances.

    :param pip_indices: Dictionary with PIP joint coordinates.
    :param mcp_indices: Dictionary with MCP joint coordinates.
    :param thresholds: Dictionary with thresholds for specific pairs and the rest.
    :return: Tuple (relative_distances, result), where:
             - normalized_distances: Dictionary of relative distances between adjacent fingertips.
             - result: Boolean indicating if all distances meet their thresholds.
    """
    adjacent_fingers = ["thumb", "index", "middle", "ring", "pinky"]
    normalized_distances = {}
    is_valid = True

    # iterate through adjacent finger pairs
    for i in range(len(adjacent_fingers) - 1):
        finger1 = adjacent_fingers[i]
        finger2 = adjacent_fingers[i + 1]

        # calculate PIP-PIP and MCP-MCP distances
        pip_distance = np.linalg.norm(np.array(pip_indices[finger1]) - np.array(pip_indices[finger2]))
        mcp_distance = np.linalg.norm(np.array(mcp_indices[finger1]) - np.array(mcp_indices[finger2]))

        # avoid division by zero for MCP distance
        if mcp_distance == 0:
            normalized_distance = float("inf")  # handle degenerate case
        else:
            # normalize pip distance using mcp distance
            normalized_distance = pip_distance / mcp_distance

        # store the normalized distance
        normalized_distances[(finger1, finger2)] = normalized_distance

        # determine the threshold for this finger pair
        if (finger1, finger2) == ("thumb", "index"):
            threshold = thresholds["thumb-index"]
        elif (finger1, finger2) == ("ring", "pinky"):
            threshold = thresholds["pinky-ring"]
        else:
            threshold = thresholds["rest"]

        # validate normalized distance against the threshold
        if normalized_distance < threshold:
            is_valid = False

    return normalized_distances, is_valid
