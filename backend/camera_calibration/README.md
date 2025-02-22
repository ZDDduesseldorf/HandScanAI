## Camera Calibration

calculates:

- brightness using the mean
- contrast using the standard deviation
- sharpness using varicance of Laplace

detects a rectangle:

- with Canny-Edge-Detection
- finds a contour with len 4
  -> 4 corner points

calculates extenisive of rectangle to check correct size
-> camera distance

### Entry point

to create calibration file use create_calibration_file(image_path, file_name, detected_rectangle) from kalibrierung.py

to check calibration of actual image use check_kalibration(image_path, file_name, detected_rectangle) from kalibrierung.py

detected_rectangle use True, when you want to detect a rectangle for calibration

### Functionality

Image quality

Brightness and contrast can be determined using the histogram of an image

The brightness is described by the average value. The higher the average value, the brighter the image. Normally, a ‘perfect’ average value is 128, as our images have a very high proportion of white, this is significantly higher in our case

The contrast is described by the scattering. The greater the scattering, the higher the contrast of the image

The sharpness of the image is determined by Laplace's variance. This describes the edge activity in the image. The higher the values, the stronger the edge presence, the sharper the image.

Rectangle detection:

In order to always have a similar image section, a calibration rectangle is placed. This is used to determine the position and circumference.
A similar perimeter ensures that the distance to the camera is similar and therefore the entire hand can be placed in the camera field.

1. conversion to greyscale image
2. gaussian blur to reduce noise
3. edge detection with Canny
4. finding contours
5. simplification by removing close points
6. if contour has 4 points it is a rectangle
