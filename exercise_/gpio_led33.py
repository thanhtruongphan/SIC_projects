from gpiozero import LED

led_red = LED(13)

while True:
	s = input()
	if s == "on":
		led_red.on()
	elif s == "off":
		led_red.off()
	else:
		print("invalid command")
