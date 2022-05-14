#!/usr/bin/python3

# import imu
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
import cv2
# from git import Repo
from picamera2.picamera2 import Picamera2

def showImageAndExit(image):
    cv2.imshow("Image", image)
    cv2.waitKey(6000)
    cv2.destroyAllWindows()
    exit(1)

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
hsvThresholds = [0, 66, 60, 255, 0, 255] # [90,120,0,255,0,255]
waterThresholds = [20,94,99]

# Image processor
imgrec = imgrec.ImgRec()

while True:
    time.sleep(2)
    (q_w, q_x, q_y, q_z) = sensor.quaternion    
    
    if (abs(q_x) < threOrien and abs(q_y) < threOrien):
        print("Facing downwards")

        # TAKE PHOTO
        image_fullsize = picam2.capture_array()
        # print(np_array)
        
        # Scale image down to Y<=1024
        image_size = image_fullsize.shape
        img_factor = 1024.0 / float(image_size[0])
        image = cv2.resize(image_fullsize, (int(image_size[1] * img_factor), 1024))
        
        # Process Image
        result = imgrec.processImage(image = image, hsvThresholds = hsvThresholds, waterThresholds = waterThresholds)
        print(result)
        
        if result[0] != 'PLASTIC':
            continue
        
        # Save Image
        t = time.strftime("_%H:%M:%S")    # current time string
        imgName = ('/home/pi/cubesat/pi-images/image_%s.jpg' % (t))
        print('Saving image to ' + imgName)
        cv2.imwrite(imgName, image)

        #if analysis[1] == 'PLASTIC':
        #    i = 1 # DELETE THIS LATER

            # SEND PHOTO
            ## BLUETOOTH CODE HERE


    else:
        print("Not facing downwards")
    
