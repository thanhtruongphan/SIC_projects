from picamera2 import Picamera2
from time import sleep
import cv2

picam2 = Picamera2()
#picam2.preview_configuration.main.size=(1920, 1080) #max (3280, 2464)
picam2.preview_configuration.sensor.output_size = (3280,2464)
picam2.preview_configuration.main.size = (800, 600)
picam2.configure("preview")

#picam2.start(show_preview=True)

while True:
	im = picam2.capture_array()
	cv2.imshow("preview", im)
	if cv2.waitKey(1) == ord('q'):
		break

picam2.stop()
cv2.destroyAllWindows()
