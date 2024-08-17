import sys
import time
import board
import adafruit_dht
import pymysql
# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D4)
# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)
db, cur = None, None
db = pymysql.connect(host='192.168.1.4', user='root', password='1234', db='mysql', charset='utf8')
try: 
    cur = db.cursor()
    while True:
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
        data = (temperature, humidity)
        if humidity is not None and temperature is not None:
            sql = "INSERT INTO temperature(temp, humid) VALUES (%4.1f, %4.1f)" % data
            print(sql)
            cur.execute(sql)
            db.commit()
        else:
            print('Failed to get reading. Try again!')
        time.sleep(2)
except KeyboardInterrupt:
    pass
finally:
    db.close()
# while True:
#     try:
#         # Print the values to the serial port
#         temperature_c = dhtDevice.temperature
#         temperature_f = temperature_c * (9 / 5) + 32
#         humidity = dhtDevice.humidity
#         print(
#             "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
#                 temperature_f, temperature_c, humidity
#             )
#         )

#     except RuntimeError as error:
#         # Errors happen fairly often, DHT's are hard to read, just keep going
#         print(error.args[0])
#         time.sleep(2.0)
#         continue
#     except Exception as error:
#         dhtDevice.exit()
#         raise error

#     time.sleep(2.0)
