from picamera2 import Picamera2 as PiCamera, Preview
from time import sleep

camera = PiCamera()
camera_config = camera.create_still_configuration(main={"size":(1920,1080)}, lores={"size":(640,480)})
camera.configure(camera_config)
camera.start_preview()
camera.start()
sleep(7)
camera.capture_file("test2.jpg")
print("done")

