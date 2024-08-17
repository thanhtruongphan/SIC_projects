from picamera2 import Picamera2 

picam2 = Picamera2()
picam2.preview_configuration.main.size=(1080,720) #(3280, 2464)
picam2.preview_configuration.main.format = "RGB888"
picam2.start()

import cv2
import numpy as np

def nothing(x):
    pass

cv2.namedWindow('marking')

cv2.createTrackbar('H Lower','marking',0,179,nothing)
cv2.createTrackbar('H Higher','marking',179,179,nothing)
cv2.createTrackbar('S Lower','marking',0,255,nothing)
cv2.createTrackbar('S Higher','marking',255,255,nothing)
cv2.createTrackbar('V Lower','marking',0,255,nothing)
cv2.createTrackbar('V Higher','marking',255,255,nothing)


while True:
    # Capture frame-by-frame
#    ret, frame = cap.read()
    # if frame is read correctly ret is True
    frame = picam2.capture_array()
    img = cv2.flip(frame,1)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hL = cv2.getTrackbarPos('H Lower','marking')
    hH = cv2.getTrackbarPos('H Higher','marking')
    sL = cv2.getTrackbarPos('S Lower','marking')
    sH = cv2.getTrackbarPos('S Higher','marking')
    vL = cv2.getTrackbarPos('V Lower','marking')
    vH = cv2.getTrackbarPos('V Higher','marking')

    LowerRegion = np.array([hL,sL,vL],np.uint8)
    upperRegion = np.array([hH,sH,vH],np.uint8)

    redObject = cv2.inRange(hsv,LowerRegion,upperRegion)

    kernal = np.ones((1,1),"uint8")

    red = cv2.morphologyEx(redObject,cv2.MORPH_OPEN,kernal)
    red = cv2.dilate(red,kernal,iterations=1)

    res1=cv2.bitwise_and(img, img, mask = red)


    cv2.imshow("Masking ",res1)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        picam2.release()
        picam2.stop()
        cv2.destroyAllWindows()
        break