#!/usr/bin/python3

#import libraries
import math
import time
import os
import board
import busio
import adafruit_bno055
#from git import Repo

#setup imu and camera
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

#SET THRESHOLD for orientation in degrees
threOrien = float(0.07)

# Assume starting orientation is 0.0
startX = float(0.0)
startY = float(0.0)

while True:
    (q_w, q_x, q_y, q_z) = sensor.quaternion    
    if (abs(q_x) < threOrien and abs(q_y) < threOrien):
        print("Facing downwards")
        # TAKE PHOTO CODE HERE
    else:
        print(" ")
    time.sleep(0.5)
    # print("%u %u %u " % (oriX, oriY, oriZ))
