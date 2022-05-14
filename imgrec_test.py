import cv2 as cv
import os
import numpy as np
import imgrec
imgrec = imgrec.ImgRec()

org = (50,50)

directory = 'pi-images-demo/'
imageList = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory,f))]

hsvThresholdsHere = [0, 66, 60, 255, 0, 255]
waterThresholdsHere = [20,70,97]

print (imageList)

def getHSVThresholds() :
        return hsvThresholdsHere
def getWaterThresholds() :
    return waterThresholdsHere

def processImages(imageList, hsvThresholds, waterThresholds):
    results = []

    for imgName in imageList:
        image = cv.imread(directory + imgName)
        image_small = cv.resize(image, (1333,1000))
        cv.imshow(imgName, image_small)
        result = imgrec.processImage(image_small, hsvThresholds, waterThresholds)
        cv.imshow(imgName + ' filtered', result[2])
        print("Hello")
        results.append(result)
    
    cv.waitKey(600000)
    cv.destroyAllWindows()
    return results

processImages([imageList[0]], hsvThresholdsHere, waterThresholdsHere)

while True:
    # quit if 'q' is pressed
    if  cv.waitKey(60) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()