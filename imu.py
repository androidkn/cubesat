#!/usr/bin/python3

#import libraries
import numpy as np
import math
import time
import os
import board
import busio
import adafruit_bno055
from git import Repo
from picamera import PiCamera

#setup imu and camera
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)
camera = PiCamera()

#SET THRESHOLD for orientation in degrees
threOrien = float(0.07)

# Assume starting orientation is 0.0
startX = float(0.0)
startY = float(0.0)


#bonus: function for uploading image to Github
def git_push():
    try:
        repo = Repo('/androidkn/cubesat')
        #PATH TO YOUR GITHUB REPO
        repo.git.add('/pi-images')
        #PATH TO YOUR IMAGES FOLDER WITHIN YOUR GITHUB REPO
        repo.index.commit('New Photo')
        print('made the commit')
        origin = repo.remote('origin')
        print('added remote')
        origin.push()
        print('pushed changes')
    except:
        print('Couldn\'t upload to git')

while True:
    (q_w, q_x, q_y, q_z) = sensor.quaternion    
    if (abs(q_x) < threOrien and abs(q_y) < threOrien):
        print("Facing downwards")
        # TAKE PHOTO CODE HERE
        name = "FlatEarthers"     #Last Name, First Initial  ex. FoxJ
        if name:
            t = time.strftime("_%H%M%S")      # current time string
            imgname = ('/home/pi/FlatSat/Images/%s%s' % (name,t)) #change directory to your folder
            camera.capture(imgname)
    else:
        print(" ")
    time.sleep(0.5)
    # print("%u %u %u " % (oriX, oriY, oriZ))
