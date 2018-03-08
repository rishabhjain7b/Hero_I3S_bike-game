import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

Relay_PIN = 4

GPIO.setup(Relay_PIN, GPIO.OUT)

GPIO.output(Relay_PIN, GPIO.HIGH)
time.sleep(5)
GPIO.output(Relay_PIN, GPIO.LOW)
GPIO.cleanup()
