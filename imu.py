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

#bonus: function for uploading image to Github
def git_push():
    try:
        repo = Repo('/home/pi/FlatSatChallenge')
        #PATH TO YOUR GITHUB REPO
        repo.git.add('folder path')
        #PATH TO YOUR IMAGES FOLDER WITHIN YOUR GITHUB REPO
        repo.index.commit('New Photo')
        print('made the commit')
        origin = repo.remote('origin')
        print('added remote')
        origin.push()
        print('pushed changes')
    except:
        print('Couldn\'t upload to git')
 
#SET THRESHOLD for orientation in degrees
threOrien = float(1.0)
#read acceleration
while True:
    oriX, oriY, oriZ = sensor.orientation
    roll = oriX;
    pitch = oriY;
    yaw = oriZ;
    # Convert into quanternion and find the rotation angle
    cyaw = math.cos(yaw * 0.5);
    syaw = math.sin(yaw * 0.5);
    cpitch = math.cos(pitch * 0.5);
    spitch = math.sin(pitch * 0.5);
    croll = math.cos(roll * 0.5);
    sroll = math.sin(roll * 0.5);

    q_w = croll * cpitch * cyaw + sroll * spitch * syaw;
    q_x = sroll * cpitch * cyaw - croll * spitch * syaw;
    q_y = croll * spitch * cyaw + sroll * cpitch * syaw;
    q_z = croll * cpitch * syaw - sroll * spitch * cyaw;
    q=np.array([q_w,q_x,q_y,q_z])

    #simple rotation angle
    alpha = 2*math.acos(q[0])*180/np.pi
    
    #CHECK IF READINGS ARE ABOVE THRESHOLD
    #if abs(oriX) < threOrien and abs(oriY) < threOrien and abs(oriZ) < threOrien:
    if abs(alpha) < threOrien:
        #PAUSE
        #TAKE/SAVE/UPLOAD A PICTURE
        name = "FlatEarthers"     #Last Name, First Initial  ex. FoxJ
        if name:
            t = time.strftime("_%H%M%S")      # current time string
            imgname = ('/home/pi/FlatSat/Images/%s%s' % (name,t)) #change directory to your folder
            camera.capture(imgname)

    #PAUSE
