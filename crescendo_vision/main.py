from .camera import Camera
import cv2

print('FRC Team 4533 "Phoenix" -- 2024 Crescendo Vision')

# Initialize the camera
cam = Camera()

# Start capturing I guess
cam.start_cap()

#####
# Put the OpenCV stuff here
#####

# Stop capturing
cam.stop_cap()
