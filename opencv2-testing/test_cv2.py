#!/usr/bin/python3

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

# Initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 15
camera.rotation = 180
rawCapture = PiRGBArray(camera, size=(320, 240))

# Allow the camera to warmup
time.sleep(2)

# Fix the camera's values so the images are consistent
camera.iso = 200
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = "off"
gains = camera.awb_gains
camera.awb_mode = "off"
camera.awb_gains = gains

# Save a previous image
previous_image = None

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array

    # turn the image into black and white
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Find differences in the images
    if previous_image is not None:
        diff_image = cv2.subtract(previous_image, gray)
        ret, diff_image = cv2.threshold(diff_image, 10, 255, cv2.THRESH_BINARY)
    else:
        diff_image = gray
        
    # Blur the image to reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Find the edges of the image
    edges = cv2.Canny(blur, 20, 30)

    # Find more edges of the image
    high_edges = cv2.Canny(blur, 60, 120)

    # Stack the images next to each other
    images = np.hstack((gray, diff_image, blur, edges, high_edges))

    # show the frame
    cv2.imshow("Frame", images)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

    previous_image = gray

