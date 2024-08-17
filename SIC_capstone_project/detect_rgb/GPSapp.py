import io
import pynmea2
import serial

# Set up the serial connection
ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

# Define the path to the file
file_path = '/home/phantt/Downloads/SIC_capstone_project/detect_rgb/gps_data.txt'

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
    
    except serial.SerialException as e:
        print(f'Device error: {e}')
        break
    except pynmea2.ParseError as e:
        print(f'Parse error: {e}')
        continue