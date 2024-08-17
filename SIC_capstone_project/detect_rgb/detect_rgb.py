from picamera2 import Picamera2 

picam2 = Picamera2()
#picam2.preview_configuration.main.size=(640,480) #max (3280, 2464)
picam2.preview_configuration.main.size= (640, 480) #(3280, 2464)

picam2.preview_configuration.main.format = "RGB888"
picam2.start()
stt_light = 0

import cv2
import numpy as np
#cap = cv.VideoCapture(1)
#if not cap.isOpened():
#    print("Cannot open camera")
#    exit()
while True:
	
	# Reading the video from the 
	# webcam in image frames 
    frame = picam2.capture_array()

	# Convert the frame in 
	# BGR(RGB color space) to 
	# HSV(hue-saturation-value) 
	# color space 
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 

	# Set range for red color and 
	# define mask 
    red_lower = np.array([120, 120, 0], np.uint8) 
    red_upper = np.array([180, 255, 255], np.uint8) 
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper) 

	# Set range for green color and 
	# define mask 
    green_lower = np.array([50, 120, 0], np.uint8) 
    green_upper = np.array([80, 255, 255], np.uint8) 
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper) 

	# Set range for blue color and 
	# define mask 
    yellow_lower = np.array([0, 120, 0], np.uint8) 
    yellow_upper = np.array([50, 255, 255], np.uint8) 
    yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper) 
	
	# Morphological Transform, Dilation 
	# for each color and bitwise_and operator 
	# between frame and mask determines 
	# to detect only that particular color 
    kernel = np.ones((5, 5), "uint8") 

	# For red color 
    red_mask = cv2.dilate(red_mask, kernel) 
    res_red = cv2.bitwise_and(frame, frame, 
							mask = red_mask) 
	
	# For green color 
    green_mask = cv2.dilate(green_mask, kernel)
    res_green = cv2.bitwise_and(frame, frame, 
								mask = green_mask) 
	
	# For blue color 
    yellow_mask = cv2.dilate(yellow_mask, kernel)
    res_yellow = cv2.bitwise_and(frame, frame, 
							mask = yellow_mask) 

	# Creating contour to track red color 
    contours, hierarchy = cv2.findContours(red_mask, 
										cv2.RETR_TREE, 
										cv2.CHAIN_APPROX_SIMPLE) 
	
    for pic, contour in enumerate(contours): 
        area_red = cv2.contourArea(contour) 
        if(area_red > 5000): 
            x, y, w, h = cv2.boundingRect(contour) 
            #frame = cv2.rectangle(frame, (x, y), 
			#						(x + w, y + h), 
			#						(0, 0, 255), 2) 
            frame = cv2.circle(frame, (int(x+w/2), int(y+h/2)), int(w/2), (0, 0, 255), 2)
            cv2.putText(frame, "Red Colour", (x, y), 
						cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
						(0, 0, 255))	 

	# Creating contour to track green color 
    contours, hierarchy = cv2.findContours(green_mask, 
										cv2.RETR_TREE, 
										cv2.CHAIN_APPROX_SIMPLE) 

    for pic, contour in enumerate(contours): 
        area_green = cv2.contourArea(contour) 
        if(area_green > 5000): 
            x, y, w, h = cv2.boundingRect(contour) 
            #frame = cv2.rectangle(frame, (x, y), 
			#						(x + w, y + h), 
			#						(0, 255, 0), 2) 
            frame = cv2.circle(frame, (int(x+w/2), int(y+h/2)), int(w/2), (0, 255, 0), 2)
            cv2.putText(frame, "Green Colour", (x, y), 
						cv2.FONT_HERSHEY_SIMPLEX, 
						1.0, (0, 255, 0))

	# Creating contour to track blue color 
    contours, hierarchy = cv2.findContours(yellow_mask, 
										cv2.RETR_TREE, 
										cv2.CHAIN_APPROX_SIMPLE) 
    for pic, contour in enumerate(contours): 
        area_yellow = cv2.contourArea(contour) 
        if(area_yellow > 5000): 
            x, y, w, h = cv2.boundingRect(contour) 
            #frame = cv2.rectangle(frame, (x, y),
			#						(x + w, y + h),
			#						(0, 255, 255), 2)
            #print(np.round(x+w/2))
            frame = cv2.circle(frame, (int(x+w/2), int(y+h/2)), int(w/2), (0, 255, 255), 2)
			
            cv2.putText(frame, "Yellow Colour", (x, y), 
						cv2.FONT_HERSHEY_SIMPLEX, 
						1.0, (0, 255, 255))



	# Program Termination
    cv2.imshow("Multiple Color Detection in Real-Time", frame) 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        picam2.release()
        picam2.stop() 
        cv2.destroyAllWindows() 
        break
