import RPi.GPIO as GPIO ## Import GPIO library
import time
import subprocess

GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(7, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
GPIO.output(7,False) ## Turn on GPIO pin 7print("Hello World")