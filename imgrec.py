import cv2 as cv
import numpy as np

org = (50,50)
imageList = ['land_water.jpg', 'land.jpg', 'water_plastic_at_edge.jpg', 'water_plastic1.jpg', 'water_plastic2.jpg', 'water.jpg']
hsvThresholds = [90,120,0,255,0,255]
waterThresholds = [20,94,99]

def percentWater(filter):
    waterPixels = np.sum(filter == 255)
    nonWaterPixels = np.sum(filter == 0)
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
        image = cv.imread('test-images/' + imgName)
        #cv.imshow(imgName, image)
        hsvImage = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        #cv.imshow(imgName, hsvImage)
        filter = cv.inRange(hsvImage, (lowH, lowS, lowV), (highH, highS, highV))
        #cv.imshow(imgName, filter)
        percent = percentWater(filter)
        result = str(imgName) + ' is most likely ' + str(findType(percent, waterThresholds)) + ' with ' + str(percent) + "% water found"
        print(result)
        results.append(result)
    
    return results

def processImage(imgName, hsvThresholds, waterThresholds):

    lowH = hsvThresholds[0]
    highH = hsvThresholds[1]
    lowS = hsvThresholds[2]
    highS = hsvThresholds[3]
    lowV = hsvThresholds[4]
    highV = hsvThresholds[5]
    
    image = cv.imread('test-images/' + imgName)
    hsvImage = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    filter = cv.inRange(hsvImage, (lowH, lowS, lowV), (highH, highS, highV))
    #cv.imshow(imgName, filter)
    percent = percentWater(filter)
    result = [imgName, findType(percent, waterThresholds), percent]
    print(str(imgName) + ' is most likely ' + str(findType(percent, waterThresholds)) + ' with ' + str(percent) + "% water found")
    return result

processImages(imageList, hsvThresholds, waterThresholds)

while True:
    # quit if 'q' is pressed
    if  cv.waitKey(60) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()