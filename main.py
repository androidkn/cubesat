import imu
import bluetooth
import imgrec

#import libraries
import numpy as np
import math
import time
import os
import board
import busio
import adafruit_bno055
from git import Repo
from picamera2.picamera2 import Picamera2


#setup imu and camera
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)
tuning = Picamera2.load_tuning_file("imx219_noir.json")
picam2 = Picamera2(tuning=tuning)
config = picam2.still_configuration()
picam2.configure(config)
picam2.start()

#SET THRESHOLD for orientation in degrees
threOrien = float(0.07)

# Assume starting orientation is 0.0
startX = float(0.0)
startY = float(0.0)

# EDIT THESE to tune model
hsvThresholds = [90,120,0,255,0,255]
waterThresholds = [20,94,99]

while True:
    (q_w, q_x, q_y, q_z) = sensor.quaternion    
    
    if (abs(q_x) < threOrien and abs(q_y) < threOrien):
        print("Facing downwards")

        # TAKE PHOTO
        np_array = picam2.capture_array()
        print(np_array)
        name = "" #EDIT NAMING OF ALL IMAGES
        if name:
            t = time.strftime("_%H%M%S")    # current time string
            imgName = ('/home/pi/Cubesat/Images/%s%s' % (name,t))
        picam2.capture_file(imgName)

        # PROCESS IMAGE
        analysis = imgrec.processImage(imgName, hsvThresholds, waterThresholds)
        if analysis[1] == 'PLASTIC':
            i = 1 # DELETE THIS LATER

            # SEND PHOTO
            ## BLUETOOTH CODE HERE

    else:
        print(" ")
    
    time.sleep(0.5)