import cv2 as cv
import numpy as np

org = (50,50)

imageList = {'land_water.jpg', 'land.jpg', 'water_plastic_at_edge.jpg', 'water_plastic1.jpg', 'water_plastic2.jpg', 'water.jpg'}

lowH = 90
highH = 120
lowS = 0
highS = 255
lowV = 0
highV = 255

minWaterPercent = 20.0
minPlasticPercent = 94.0
maxPlasticPercent = 99.0

def percentWater(filter):
    waterPixels = np.sum(filter == 255)
    nonWaterPixels = np.sum(filter == 0)
    waterPercent = round((100*waterPixels)/(waterPixels + nonWaterPixels), 3)
    return waterPercent

def findType(percent):
    if (percent < minWaterPercent):
        return 'LAND'
    elif (percent > maxPlasticPercent or percent < minPlasticPercent):
        return 'WATER'
    else:
        return 'PLASTIC'
    
for imgName in imageList:
    image = cv.imread('test-images/' + imgName)
    #cv.imshow(imgName, image)
    hsvImage = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    #cv.imshow(imgName, hsvImage)
    filter = cv.inRange(hsvImage, (lowH, lowS, lowV), (highH, highS, highV))
    cv.imshow(imgName, filter)
    percent = percentWater(filter)
    print(str(imgName) + ' is most likely ' + str(findType(percent)) + ' with ' + str(percent) + "% water found")

while True:
    # quit if 'q' is pressed
    if  cv.waitKey(60) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()