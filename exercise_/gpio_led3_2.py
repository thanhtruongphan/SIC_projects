from gpiozero import LED
import psutil
from time import sleep 
from datetime import  datetime

led_yellow = LED(6)
led_red = LED(5)
file = open("/home/phantt/Downloads/Toy_projects/cpu_usage_log.txt", "w")

while True:
	cpu_usage = psutil.cpu_percent(interval = 1, percpu = True)
	cpu_usage_mean = sum([i/len(cpu_usage) for i in cpu_usage])
	cpu_usage_mean = round(cpu_usage_mean, 3)
	print(f"cpu usage(%) : {cpu_usage_mean}%")
	if 60 > cpu_usage_mean > 30:
		led_yellow.on()
		led_red.off()
	elif cpu_usage_mean >= 60:
		led_yellow.on()
		led_red.on()
	else: 
		led_red.off()
		led_yellow.off()
	data = f"{datetime.now().strftime('%Y/%m/%d %HH %MM %SS')}  "\
		f"cpu usage(%) : {cpu_usage_mean}% \n"
	file.write(data)
	sleep(1)
file.close()
