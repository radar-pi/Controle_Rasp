import RPi.GPIO as GPIO 
from time import sleep 
rele = 8
while True:
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(rele, GPIO.OUT)

	GPIO.output(rele, GPIO.HIGH)
	print("Alto")
	sleep(0.2) 
	
	GPIO.output(rele, GPIO.LOW)
	print("Baixo") 
	 
	GPIO.cleanup()
	sleep(0.2)
