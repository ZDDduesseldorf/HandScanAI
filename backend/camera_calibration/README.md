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

to create calibration file use create_calibration_file(image_path, file_name) from kalibrierung.py

to check calibration of actual image use check_kalibration(image_path, file_name) from kalibrierung.py
