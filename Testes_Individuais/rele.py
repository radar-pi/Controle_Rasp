import RPi.GPIO as GPIO 
from time import sleep 
rele = 21
GPIO.setwarnings(False)
GPIO.setup(rele, GPIO.OUT)
while True:
	GPIO.output(rele, GPIO.HIGH)
	sleep(1) 
	GPIO.output(rele, GPIO.LOW) 
	sleep(1) 
