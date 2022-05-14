import cv2 as cv
import numpy as np

org = (50,50)
imageList = [
    'demo0001.jpg', 
    'demo0002.jpg', 
    'demo0003.jpg', 
    'demo0004.jpg', 
    'demo0005.jpg', 
    'demo0006.jpg', 
    'demo0007.jpg', 
    'demo0008.jpg', 
    'demo0009.jpg', 
    'demo0010.jpg'
]

directory = 'learning_photos/shoe2/'

hsvThresholdsHere = [0, 66, 60, 255, 0, 255]
waterThresholdsHere = [20,70,97]

def getHSVThresholds():
    return hsvThresholdsHere
def getWaterThresholds():
    return waterThresholdsHere

def percentWater(filter):
    waterPixels = np.sum(filter == 0)
    nonWaterPixels = np.sum(filter == 255)
    waterPercent = round((100*waterPixels)/(waterPixels + nonWaterPixels), 3)
    return waterPercent

def findType(percent, waterThresholds):
    minWaterPercent = waterThresholds[0]
    minPlasticPercent = waterThresholds[1]
    maxPlasticPercent = waterThresholds[2]
    if (percent < minWaterPercent):
        return 'LAND'
    elif (percent > maxPlasticPercent or percent < minPlasticPercent):
        return 'WATER'
    else:
        return 'PLASTIC'

def processImages(imageList, hsvThresholds, waterThresholds):
    results = []

    lowH = hsvThresholds[0]
    highH = hsvThresholds[1]
    lowS = hsvThresholds[2]
    highS = hsvThresholds[3]
    lowV = hsvThresholds[4]
    highV = hsvThresholds[5]

    for imgName in imageList:
        #image = cv.imread('pi-images/learning_photos/shoe2/' + imgName)
        ##cv.imshow(imgName, image)
        #hsvImage = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        ##cv.imshow(imgName, hsvImage)
        #filter = cv.inRange(hsvImage, (lowH, lowS, lowV), (highH, highS, highV))
        #cv.imshow(imgName, filter)
        #percent = percentWater(filter)
        result = processImage(imgName, hsvThresholds, waterThresholds)
        results.append(result)
    
    return results

def processImage(imgName, hsvThresholds, waterThresholds):

    lowH = hsvThresholds[0]
    highH = hsvThresholds[1]
    lowS = hsvThresholds[2]
    highS = hsvThresholds[3]
    lowV = hsvThresholds[4]
    highV = hsvThresholds[5]
    
    origImage = cv.imread(directory + imgName)
    image = cv.resize(origImage, (1333,1000))
    hsvImage = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    filter = cv.inRange(hsvImage, (lowH, lowS, lowV), (highH, highS, highV))
    cv.imshow(imgName, filter)
    percent = percentWater(filter)
    result = [imgName, findType(percent, waterThresholds), percent]
    print(str(imgName) + ' is most likely ' + str(findType(percent, waterThresholds)) + ' with ' + str(percent) + "% water found")
    return result

processImages(imageList, hsvThresholdsHere, waterThresholdsHere)

while True:
    # quit if 'q' is pressed
    if  cv.waitKey(60) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()