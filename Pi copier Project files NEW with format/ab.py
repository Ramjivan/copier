import RPi.GPIO as GPIO ## Import GPIO library
import time
import subprocess


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP) ##Push Button GPIO
GPIO.setup(40, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
GPIO.output(40,True) ## Turn on GPIO pin 7 LEDON

while True:
    input_state = GPIO.input(36)
    time.sleep(0.5)
    if input_state == False:
        subprocess.call(['./copy.sh'])
        break
    
