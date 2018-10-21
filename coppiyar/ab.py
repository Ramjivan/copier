import RPi.GPIO as GPIO ## Import GPIO library
import time
import subprocess

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(7, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
GPIO.output(7,True) ## Turn on GPIO pin 7print("Hello World")

while True:
    input_state = GPIO.input(11)
    time.sleep(1)
    if input_state == False:
        subprocess.call(['./copy.sh'])
        break
    
