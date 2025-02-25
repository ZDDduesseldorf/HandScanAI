![CI](https://github.com/ZDDduesseldorf/HandScanAI/actions/workflows/ci.yml/badge.svg?branch=main)

# HandScanAI

Building a transparent, reliable, robust AI application to predict biometric information from hand images.

## Overview

HandScanAI is an AI-powered web application for analyzing hand images. The application utilizes a Convolutional Neural Network (CNN) in combination with a vector database (Milvus) and a RandomForest algorithm to estimate the age and gender of a person based on an uploaded hand image.

## How It Works

1. **Image Capture**  
   The frontend interface allows users to take a hand image using their device's camera.

2. **Data Processing**  
   The image is sent to the backend, where it is normalized and transformed into an embedding.

3. **Analysis**  
   The embedding is compared with an existing dataset stored in the vector database (Milvus) using an Approximate Nearest Neighbors (ANN) algorithm.

4. **Result Determination**  
   A RandomForest algorithm determines the estimated age and gender based on the most similar entries.

5. **Result Display**  
   The estimated values and confidence levels are displayed in the frontend, along with reference images of similar hands.

6. **Feedback Loop**  
   Users can confirm or correct the results. If corrected, the image and metadata are stored, and the corresponding embedding is added to the vector database, improving the model over time.

## Known Limitations

The application works best under certain conditions:

- **Background**: The hand should be photographed against a white background to ensure accurate mask generation for separating the hand from the rest of the image.
- **Hand Position**: Fingers should be spread apart; otherwise, the mask might not be generated correctly.
- **Data Quality**: Distortions, shadows, or poor lighting can negatively impact recognition accuracy.
- **Dataset Bias**: The model relies on existing training data. If certain age groups or skin types are underrepresented, predictions may be less accurate.
