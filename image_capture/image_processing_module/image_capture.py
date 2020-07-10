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
stereo_clock_out_gpio = 17     # PIN 11
stereo_response_in_gpio = 18   # PIN 12
GPIO.setup(stereo_clock_out_gpio, GPIO.OUT)
GPIO.setup(stereo_response_in_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Initialize the camera and grab a reference to the raw camera capture
resolution = (320, 240)
camera = PiCamera()
camera.resolution = resolution
camera.framerate = 15
camera.rotation = 180
rawCapture = PiRGBArray(camera, size=resolution)

# Allow the camera to warmup
time.sleep(2)

# Loop forever sending clock pulses and collecting images
stereo_image_frequency_hz = 0.2
acceptable_latency_s = 0.05
while True:
    GPIO.output(stereo_clock_out_gpio, 1)
    start_time = time.time()
    print('Stereo Clock Pulsed')
    camera.capture(rawCapture, format='bgr')
    frame = rawCapture.array
    GPIO.output(stereo_clock_out_gpio, 0)
    if GPIO.input(stereo_response_in_gpio) != 1:
        GPIO.wait_for_edge(stereo_response_in_gpio, GPIO.RISING, timeout=acceptable_latency_s * 1000)
    if time.time() - start_time < acceptable_latency_s:
        print("Good images")
    else:
        print("Bad Images")
    cv2.imwrite('stereo_cap.png', frame)
    time.sleep((1 / stereo_image_frequency_hz) - (time.time() - start_time))
