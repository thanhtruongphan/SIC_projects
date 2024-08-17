# import paho.mqtt.client as mqtt
import numpy as np
import time
import cv2
from picamera2 import Picamera2

# Thiết lập camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.start()

# Thiết lập MQTT
broker = "5b3a886659fe4b0c9123bb34ac492b6b.s1.eu.hivemq.cloud"  # Thay thế bằng broker của bạn
port = 8883
topic = "traffic_light/status"

# client = mqtt.Client()
# client.connect(broker, port, 60)
# client.loop_start()

import paho.mqtt.client as mqtt

# Define callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

# Create an MQTT client instance
client = mqtt.Client()  # Đây vẫn là cách khởi tạo chính xác

# Attach callback functions
client.on_connect = on_connect

# Connect to the broker
client.connect(broker, port, 60)

# Start the network loop
client.loop_start()


def detect_color(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    red_lower = np.array([120, 120, 0])
    red_upper = np.array([180, 255, 255])
    yellow_lower = np.array([0, 120, 0])
    yellow_upper = np.array([50, 255, 255])
    green_lower = np.array([50, 120, 0])
    green_upper = np.array([80, 255, 255])

    red_mask = cv2.inRange(hsv_frame, red_lower, red_upper)
    yellow_mask = cv2.inRange(hsv_frame, yellow_lower, yellow_upper)
    green_mask = cv2.inRange(hsv_frame, green_lower, green_upper)

    red_area = cv2.countNonZero(red_mask)
    yellow_area = cv2.countNonZero(yellow_mask)
    green_area = cv2.countNonZero(green_mask)

    if red_area > yellow_area and red_area > green_area:
        return "Red"
    elif yellow_area > red_area and yellow_area > green_area:
        return "Yellow"
    elif green_area > red_area and green_area > yellow_area:
        return "Green"
    else:
        return "Unknown"

while True:
    frame = picam2.capture_array()
    color = detect_color(frame)
    payload = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {color}"
    client.publish(topic, payload)
    time.sleep(1)  # Gửi dữ liệu mỗi giây
