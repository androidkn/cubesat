import cv2 as cv
import numpy as np

class ImgRec:
    org = (50,50)
    
    
    hsvThresholdsHere = [0, 66, 60, 255, 0, 255]
    waterThresholdsHere = [20,94,99]
    
    def percentWater(self, filter):
        waterPixels = np.sum(filter == 0)
        nonWaterPixels = np.sum(filter == 255)
        waterPercent = round((100*waterPixels)/(waterPixels + nonWaterPixels), 3)
        return waterPercent
    
    def findType(self, percent, waterThresholds):
        minWaterPercent = waterThresholds[0]
        minPlasticPercent = waterThresholds[1]
        maxPlasticPercent = waterThresholds[2]
        if (percent < minWaterPercent):
            return 'LAND'
        elif (percent > maxPlasticPercent or percent < minPlasticPercent):
            return 'WATER'
        else:
            return 'PLASTIC'
    

    def processImage(self, image, hsvThresholds, waterThresholds):
        lowH = hsvThresholds[0]
        highH = hsvThresholds[1]
        lowS = hsvThresholds[2]
        highS = hsvThresholds[3]
        lowV = hsvThresholds[4]
        highV = hsvThresholds[5]
        
        hsvImage = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        filter = cv.inRange(hsvImage, (lowH, lowS, lowV), (highH, highS, highV))
        percent = self.percentWater(filter)
        result = [self.findType(percent, waterThresholds), percent, filter]
        #print(' is most likely ' + str(self.findType(percent, waterThresholds)) + ' with ' + str(percent) + "% water found")
        return result
