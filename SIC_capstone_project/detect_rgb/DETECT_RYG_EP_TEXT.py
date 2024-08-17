# import cv2
import numpy as np
import time
import cv2
from picamera2 import Picamera2 

picam2 = Picamera2()
picam2.preview_configuration.main.size=(640,480) #max (3280, 2464)
picam2.preview_configuration.main.format = "RGB888"
picam2.start()
# Khởi động camera
# camera = cv2.VideoCapture(0)


def detect_color(frame):
    # 
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 
    red_lower = np.array([120, 120, 0])
    red_upper = np.array([180, 255, 255])

    yellow_lower = np.array([0, 120, 0])
    yellow_upper = np.array([50, 255, 255])

    green_lower = np.array([50, 120, 0])
    green_upper = np.array([80, 255, 255])

    # 
    red_mask = cv2.inRange(hsv_frame, red_lower, red_upper)
    yellow_mask = cv2.inRange(hsv_frame, yellow_lower, yellow_upper)
    green_mask = cv2.inRange(hsv_frame, green_lower, green_upper)

    # 
    red_area = cv2.countNonZero(red_mask)
    yellow_area = cv2.countNonZero(yellow_mask)
    green_area = cv2.countNonZero(green_mask)

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

    # Xác định màu sắc có diện tích lớn nhất
    if red_area > yellow_area and red_area > green_area:
        return "Red"
    elif yellow_area > red_area and yellow_area > green_area:
        return "Yellow"
    elif green_area > red_area and green_area > yellow_area:
        return "Green"
    else:
        return "Unknown"

while True:
    # ret, frame = camera.read()
    frame = picam2.capture_array()

    # if not ret:
    #     print("Camera not found.")
    #     break

    # Nhận diện màu sắc
    color = detect_color(frame)
    print(f"Color current: {color}")
    # print(type(color))

    # Ghi kết quả vào file (ghi đè để chỉ lưu lại trạng thái mới nhất)
    with open("/home/phantt/Downloads/SIC_capstone_project/detect_rgb/traffic_light_status.txt", "w") as file:
        file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {color}\n")
        # file.write(f"{color}\n")
    # show hinh
    cv2.imshow("Traffic Light Detection", frame)

    # Thoát khi nhấn phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop()
# Giải phóng tài nguyên
# camera.release()
cv2.destroyAllWindows()
