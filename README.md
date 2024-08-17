# SIC_projects
>> Do all of comment line on virtual environment...

### Switch to 'master' branch to see the project...

### To install picamera2 (using on Raspberry pi 4B, PiOS bookworm 64 bit)
- picamera2 default install with piOS bookworm
B1: create virtual environment with comment line in the first folder default:

>>> python -m venv --system-site-packages env
>>> source env/bin/activate

B2: test camera with comment line: 

>>> python3 "name_of_file_python" /or sudo python3 "name_of_file_python"

Note: follow link documentation "https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf" or code:

> To install opencv, follow this link: https://pypi.org/project/opencv-python/#manual-builds
>>> pip install opencv-contrib-python
##### start code
import cv2
from picamera2 import Picamera2 

picam2 = Picamera2()
picam2.preview_configuration.main.size=(640,480) #max of Camera PiV2 is (3280, 2464)
picam2.preview_configuration.main.format = "RGB888"
picam2.start()

while True:
	im = picam2.capture_array()
	cv2.imshow("preview", im)
	if cv2.waitKey(1) == ord('q'):
		break

picam2.stop()
cv2.destroyAllWindows()
##### End code

Note: Must run the code on Terminal of VNC-viewer or similar, because some IDE like VScode doesn't, it show "Available platform plugins are: eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, wayland-egl, wayland, wayland-xcomposite-egl, wayland-xcomposite-glx, xcb.

Aborted"


### To using MQTT

B1: install paho-mqtt library. Follow this link: https://console.hivemq.cloud/clients/python-paho

Note: install paho-mqtt<2.0 like "pip3 install paho-mqtt==1.5.1"
Or Follow this link: https://github.com/hivemq-cloud/paho-mqtt-client-example/blob/master/requirements.txt

B2: code example in here: https://github.com/hivemq-cloud/paho-mqtt-client-example/blob/master/simple_example.py

There are 4 things we need to see: 
client.username_pw_set("<your_username>", "<your_password>")
client.connect("<your_host>", 8883)

B3: create account MQTT broker (example HiveMQ) like: 
- Go to "https://www.hivemq.com/
- next "Login"
- Create a free Cluster
![image](https://github.com/user-attachments/assets/5e9bce24-ffad-46bd-a1d8-4b58dfd10051)
- ULR is hostname
- Port 8883
- Click "Manage Cluster" -> "Client"
![image](https://github.com/user-attachments/assets/42aa106c-0f0e-4a7b-822b-b84cffeaf6be)
- Autocreate account... then we need to remember this!
- Next subcribe all the topic "#"
![image](https://github.com/user-attachments/assets/da60b03d-0026-4043-be0a-137dbfc527a0)

### To sent data on Broker/Cluster to Web...
...waiting to write...


### to use 'Neo 6M GPS sensor' with MQTT broker HiveMQ
- Follow this link: https://sparklers-the-makers.github.io/blog/robotics/use-neo-6m-module-with-raspberry-pi/

Note: Fix problem "ERROR V4L2 v4l2_videodevice.cpp:1906 /dev/video0[18:cap]: Failed to start streaming: Invalid argument"
> follow this link: https://github.com/raspberrypi/libcamera/issues/104
![image](https://github.com/user-attachments/assets/a6ab3abc-87ca-4a1b-9518-9bcf46997492)

OK.
Result...:
![image](https://github.com/user-attachments/assets/75d301e2-0262-43d9-ac70-7d4c96331fd6)
![image](https://github.com/user-attachments/assets/7294b3e2-2400-41b8-8084-c8d77d5da37e)

> Code file GPS_PUB_SUB.py



### Image processing, Detect Red-Yellow-Green real-time with MQTT broker HiveMQ

> Code file DETECT_RYB_PUBSUB.py


