from gpiozero import LED

led_red = LED(13)

while True:
	led_red.on()
