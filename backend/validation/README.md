# Validation

## Overview

The validation pipeline checks whether an image meets specific criteria.  
These checks include:

- **Hand is Visible** – Ensures the hand is present in the image.
- **Hand is Dorsal** – Verifies that the back of the hand is facing the camera.
- **Hand is Spread** – Confirms that the fingers are sufficiently separated.

The validation pipeline returns a dictionary containing the results of each test.  
All tests rely on the **MediaPipe Hand Landmarks Model**.

## How to Use

1. Pass an image to `validation_pipeline()`.  
2. The resulting dictionary contains the validation results.  
3. To automatically check if all tests passed, pass the dictionary to `is_validation_pipeline_valid()`.  
