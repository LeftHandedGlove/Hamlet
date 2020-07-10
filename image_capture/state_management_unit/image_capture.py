#!/usr/bin/python3

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import RPi.GPIO as GPIO
import atexit

# Set the mode to use chip GPIO numbering
GPIO.setmode(GPIO.BCM)
atexit.register(GPIO.cleanup)

# Setup the GPIOs
stereo_clock_in_gpio = 17     # PIN 11
stereo_response_out_gpio = 18  # PIN 12
GPIO.setup(stereo_clock_in_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(stereo_response_out_gpio, GPIO.OUT)

# Initialize the camera and grab a reference to the raw camera capture
resolution = (320, 240)
camera = PiCamera()
camera.resolution = resolution
camera.framerate = 15
camera.rotation = 180
rawCapture = PiRGBArray(camera, size=resolution)

# Allow the camera to warmup
time.sleep(2)

# Loop forever waiting for clock pulses
while True:
    GPIO.wait_for_edge(stereo_clock_in_gpio, GPIO.RISING)
    print('Stereo Clock Pulse Received')
    camera.capture(rawCapture, format='bgr')
    frame = rawCapture.array
    GPIO.output(stereo_response_out_gpio, 1)
    cv2.imwrite('stereo_cap.png', frame)
    time.sleep(0.1)
    GPIO.output(stereo_response_out_gpio, 0)
