#
# Copyright 2021 HiveMQ GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import time

import paho.mqtt.client as paho
from paho import mqtt


# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    """
        Prints the result of the connection with a reasoncode to stdout ( used as callback for connect )

        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param flags: these are response flags sent by the broker
        :param rc: stands for reasonCode, which is a code for the connection result
        :param properties: can be used in MQTTv5, but is optional
    """
    print("CONNACK received with code %s." % rc)


# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    """
        Prints mid to stdout to reassure a successful publish ( used as callback for publish )

        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param mid: variable returned from the corresponding publish() call, to allow outgoing messages to be tracked
        :param properties: can be used in MQTTv5, but is optional
    """
    print("mid: " + str(mid))


# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    """
        Prints a reassurance for successfully subscribing

        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param mid: variable returned from the corresponding publish() call, to allow outgoing messages to be tracked
        :param granted_qos: this is the qos that you declare when subscribing, use the same one for publishing
        :param properties: can be used in MQTTv5, but is optional
    """
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    """
        Prints a mqtt message to stdout ( used as callback for subscribe )

        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param msg: the message with topic and payload
    """
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("hivemq.webclient.1723605366923", "34HAZOGayun68,<Nl%d#")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("85334ea20e91412da2bcf2c26bf7e321.s1.eu.hivemq.cloud", 8883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# subscribe to all topics of encyclopedia by using the wildcard "#"
client.subscribe("paho/test/multiple", qos=1)

# a single publish, this can also be done in loops, etc.
client.publish("paho/test/multiple", payload="kiem tra pubsub", qos=1)

# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop
# client.loop_forever()

# xxxxxxxxxxxxxxxxxxxxxxxxxx #
import numpy as np
import time
import cv2
from picamera2 import Picamera2 

picam2 = Picamera2()
picam2.preview_configuration.main.size=(640,480) #max of CameraPiV2 is (3280, 2464)
picam2.preview_configuration.main.format = "RGB888"
picam2.start()
# Khởi động camera


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
    # if not ret:
    #     print("Camera not found.")
    #     break
    frame = picam2.capture_array()
    
    # Nhận diện màu sắc
    color = detect_color(frame)
    print(f"Color current: {color}")

    # Ghi kết quả vào file (ghi đè để chỉ lưu lại trạng thái mới nhất)
    with open("/home/truongpt/Downloads/SIC_capstones/traffic_light_status.txt", "w") as file:
        # file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {color}\n")
        file.write(color)
    with open("/home/truongpt/Downloads/SIC_capstones/traffic_light_status.txt", "r") as file:
        result = str(file.readline())
    client.loop_start()
    client.publish("paho/test/multiple", payload=result, qos=1)
    client.loop_stop()
    # show hinh
    cv2.imshow("Traffic Light Detection", frame)

    # Thoát khi nhấn phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# dừng camera và giải phóng tài nguyên 
picam2.stop()
# camera.release()
cv2.destroyAllWindows()
