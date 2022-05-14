#!//usr/bin/python3

from picamera2.picamera2 import Picamera2
import time
import cv2

tuning = Picamera2.load_tuning_file("imx219_noir.json")

picam2 = Picamera2(tuning=tuning)
# picam2 = Picamera2()
config = picam2.still_configuration()
picam2.configure(config)

picam2.start()

# np_array = picam2.capture_array()
# print(np_array)

i = 1

while i < 100:
	filename = "demo" + str(i).zfill(4) + ".jpg"
	picam2.capture_file(filename)
	print('Captured ' + filename)
	image = cv2.imread(filename)
	n_img = cv2.putText(image, filename, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (127, 127, 0), 2, cv2.LINE_AA)
	cv2.imshow("Preview", n_img)
	i = i + 1
	time.sleep(1)

picam2.stop()

