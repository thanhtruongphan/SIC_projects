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
client.subscribe("paho/test/gps", qos=1)

# a single publish, this can also be done in loops, etc.
client.publish("paho/test/gps", payload="kiem tra pubsub gps", qos=1)

# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop
# client.loop_forever()




import io
import pynmea2
import serial

# Set up the serial connection
ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

# Define the path to the file
file_path = '/home/truongpt/Downloads/SIC_capstones/gps_data.txt'

# Main loop to read and parse NMEA sentences
while True:
    try:
        line = sio.readline()
        msg = pynmea2.parse(line)
        
        # Only process RMC sentences since they contain speed
        if isinstance(msg, pynmea2.types.talker.RMC):
            latitude = msg.latitude
            longitude = msg.longitude
            speed_knots = msg.spd_over_grnd  # Speed in knots
            speed_kmh = speed_knots * 1.852  # Convert speed to km/h
            speed_kmh_int = int(round(speed_kmh))  # Convert speed to integer (rounded)
            
            # Format the output string
            output_w = f"Latitude: {latitude}, Longitude: {longitude}, Speed (km/h): {speed_kmh_int}\n"
            output = f"{latitude}, {longitude}, {speed_kmh_int}\n"            
            # Write to the file, overwriting previous content
            with open(file_path, 'w') as file:
                file.write(output)
                # file.write(latitude,' ',longitude,' ',speed_kmh_int)
            # Optionally, print to the console as well
            print(output_w)
            client.loop_start()
            client.publish("paho/test/gps", payload=output, qos=1)
            client.loop_stop()
    
    except serial.SerialException as e:
        print(f'Device error: {e}')
        break
    except pynmea2.ParseError as e:
        print(f'Parse error: {e}')
        continue
