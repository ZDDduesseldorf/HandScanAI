![CI](https://github.com/ZDDduesseldorf/HandScanAI/actions/workflows/ci.yml/badge.svg?branch=main)

# HandScanAI

Building a transparent, reliable, robust AI application to predict biometric information from hand images.

## Overview

HandScanAI is an AI-powered web application for analyzing hand images. The application utilizes a Convolutional Neural Network (CNN) in combination with a vector database (Milvus) and a k-Nearest-Neighbours algorithm to estimate the age and gender of a person based on an uploaded hand image

The goal of this project is to create a simple and intuitive application that can be easily explained to non-experts, making it ideal for exhibitions, educational settings, and public demonstrations.

## How It Works

1. **Image Capture**  
   The frontend interface allows users to take a hand image using their device's camera. For current limitations see [Known Limitations](#known-limitations)


2. **Data Processing**  
   The image is sent to the backend, where it is normalized and transformed into an embedding.

3. **Distance Calculation & Classification**  
   The embedding is compared with an existing dataset stored in the vector database and classified using a k-Nearest Neighbours algorithm. 

4. **Result Display**  
   The estimated values and confidence levels are displayed in the frontend, along with reference images of similar hands.

5. **Feedback Loop**  
   Users can confirm or correct the results. Then the image and metadata are stored, and the corresponding embedding is added to the vector database, improving the model over time.

## System Architecture

HandScanAI consists of a **frontend** and a **backend**, where the backend can also be used **independently** without the frontend.  

### **Architecture Diagram**
Below is a high-level system architecture diagram illustrating the main components and interactions of HandScanAI:

![HandScanAI Architecture](readme_data/HandScanAIArchitecture.png)

### Project Components

- **Frontend:** A modern web application built with React, TypeScript, Vite, Material UI, and Emotion.  
  Detailed setup, development, and build instructions can be found in the **[Frontend README](frontend/README.md)**.

- **Backend:** A Python and FastAPI backend managing data processing, API endpoints, and AI functionalities.
  Utilized technologies are MediaPipe, OpenCV, PyTorch-CNNs, and Milvus.
  For installation, development, and deployment instructions, see the **[Backend README](backend/README.md)**.


## Known Limitations

The application works best under certain conditions:

- **Background**: The hand should be photographed against a white background to ensure accurate mask generation for separating the hand from the rest of the image.
- **Hand Position**: Fingers should be spread apart; otherwise, the mask might not be generated correctly.
- **Data Quality**: Distortions, shadows, or poor lighting can negatively impact recognition accuracy.
- **Dataset Bias**: The model relies on existing training data. If certain age groups or skin types are underrepresented, predictions may be less accurate.

