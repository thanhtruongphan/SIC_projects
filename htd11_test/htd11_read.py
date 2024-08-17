import Adafruit_DHT
import time

# Ð?nh nghia lo?i c?m bi?n và chân k?t n?i
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 48

def compute_heat_index(temperature, humidity, is_fahrenheit=True):
    # Tính toán ch? s? nhi?t
    if is_fahrenheit:
        hi = temperature
    else:
        hi = temperature * 9/5 + 32  # Chuy?n d?i t? C sang F n?u c?n

    c1 = -42.379
    c2 = 2.04901523
    c3 = 10.14333127
    c4 = -0.22475541
    c5 = -0.00683783
    c6 = -0.05481717
    c7 = 0.00122874
    c8 = 0.00085282
    c9 = -0.00000199

    heat_index = (c1 + (c2 * hi) + (c3 * humidity) + (c4 * hi * humidity) +
                  (c5 * hi ** 2) + (c6 * humidity ** 2) + (c7 * hi ** 2 * humidity) +
                  (c8 * hi * humidity ** 2) + (c9 * hi ** 2 * humidity ** 2))

    if not is_fahrenheit:
        heat_index = (heat_index - 32) * 5/9  # Chuy?n d?i t? F sang C n?u c?n

    return heat_index

def main():
    print("DHTxx test!")

    while True:
        # Ð?c giá tr? d? ?m và nhi?t d?
        humidity, temperature_c = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        temperature_f = temperature_c * 9/5 + 32

        # Ki?m tra xem có l?i khi d?c không
        if humidity is None or temperature_c is None or temperature_f is None:
            print("Failed to read from DHT sensor!")
            time.sleep(2)
            continue

        # Tính toán ch? s? nhi?t
        heat_index_f = compute_heat_index(temperature_f, humidity)
        heat_index_c = compute_heat_index(temperature_c, humidity, is_fahrenheit=False)

        # In ra k?t qu?
        print(f"Humidity: {humidity:.1f}%  Temperature: {temperature_c:.1f}°C {temperature_f:.1f}°F  Heat index: {heat_index_c:.1f}°C {heat_index_f:.1f}°F")

        # Ð?i vài giây tru?c khi do ti?p
        time.sleep(2)

if __name__ == "__main__":
    main()
