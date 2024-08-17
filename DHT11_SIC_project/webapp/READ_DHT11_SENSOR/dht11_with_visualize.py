

import time
import board
import adafruit_dht
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import matplotlib

# Debugging: Print the current Matplotlib backend
print("Using Matplotlib backend:", matplotlib.get_backend())

fig = plt.figure()
ax = plt.axes(xlim=(0, 30), ylim=(15, 45))
max_points = 30
line, = ax.plot(np.arange(max_points),
                np.ones(max_points, dtype=np.float64)*np.nan, lw=1, c='blue', marker='d', ms=2)

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D4, use_pulseio=True)
def init():
    line.set_ydata(np.ones(max_points, dtype=np.float64)*np.nan)
    return line,

def animate(i):
    try:
        temperature_c = dhtDevice.temperature
        print(f"Temperature: {temperature_c}°C")  # Debugging: Print temperature
        if temperature_c is not None:
            old_y = line.get_ydata()
            new_y = np.r_[old_y[1:], temperature_c]
            line.set_ydata(new_y)
    except RuntimeError as error:
        # Handle errors by printing them (or logging)
        print("Error reading from DHT11 sensor:", error.args[0])
    return line,
anim = animation.FuncAnimation(fig, animate, init_func=init, frames=200, interval=1000, blit=True)
plt.show()


######-------------------------------------------------################


# # SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# # SPDX-License-Identifier: MIT

# import time
# import board
# import adafruit_dht

# from matplotlib import pyplot as plt
# from matplotlib import animation
# import numpy as np

# fig = plt.figure()
# ax = plt.axes(xlim=(0, 30), ylim=(15, 45))
# max_points = 30
# line, = ax.plot(np.arange(max_points),
#                 np.ones(max_points, dtype=np.float64)*np.nan, lw=1, c='blue', marker='d', ms=2)

# # Initial the dht device, with data pin connected to:
# dhtDevice = adafruit_dht.DHT11(board.D4)
# # print(dhtDevice.temperature)

# def init():
#     return line
# temperature_c = dhtDevice.temperature

# def animate(i):
#     temperature_c = dhtDevice.temperature
#     y = temperature_c
#     old_y = line.get_ydata()
#     new_y = np.r_[old_y[1:], y]
#     line.set_ydata(new_y)
#     return line,

# anim = animation.FuncAnimation(fig, animate, init_func=init, frames=200, interval=20, blit=False)
# plt.show()
#----------------------------------------------------------------------------------------########

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

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

#     ###########
