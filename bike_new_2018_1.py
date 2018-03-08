import subprocess
import os
import socket
import telnetlib
import time
import sys
from os import system
import RPi.GPIO as GPIO
import math
import serial

ser = serial.Serial('/dev/ttyAMA0', 9600)

GPIO.setmode(GPIO.BCM)

PRO_LEFT_LOG_RIGHT = 23
PRO_RIGHT_LOG_LEFT = 24
Clutch_PIN = 9
Gear_PIN = 10
Brake_PIN = 11
Sensor_PIN = 25 
BRAKE = 0
GEAR = 0
CLUTCH = 0
direction = 0
velocity = 0 

GPIO.setup(PRO_LEFT_LOG_RIGHT, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(PRO_RIGHT_LOG_LEFT, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(Clutch_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(Gear_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(Brake_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

while True:
	
		serial_line = ser.readline()
		print(serial_line)
		time.sleep(0.02)
				
		if GPIO.input(PRO_LEFT_LOG_RIGHT) == False and GPIO.input(PRO_RIGHT_LOG_LEFT) == True:
			direction = 1      		#left													#LEFT sensor is ACTIVE HIGH, RIGHT sensor is ACTIVE HIGH
					
		if GPIO.input(PRO_LEFT_LOG_RIGHT) == True and GPIO.input(PRO_RIGHT_LOG_LEFT) == False:
			direction = 2			#right
				
		if GPIO.input(PRO_LEFT_LOG_RIGHT) == True and GPIO.input(PRO_RIGHT_LOG_LEFT) == True:
			direction = 0			#centre
						
		if GPIO.input(Brake_PIN) == True:
			BRAKE = 1					#Brake_ON
				
		else:
			BRAKE = 0					#Brake_OFF
					   					   	   
		if GPIO.input(Clutch_PIN) == True:
			CLUTCH = 0					#CLUTCH_ON (Pressed)

		else:
			CLUTCH = 1					#CLUTCH_OFF (Not_Pressed)
			
		if GPIO.input(Gear_PIN) == True:
			GEAR = 1					#In Gear

		else:
			GEAR = 0					#Neutral
		   
		velocity =int(serial_line)
		if velocity <= 0:
			velocity = 0
		print +velocity,""+str(GEAR),""+str(CLUTCH),""+str(BRAKE),""+str(direction)
		
		tn = telnetlib.Telnet()
		if tn.open("169.254.178.66","1080"):
			try:
				print "Ready"
				tn.write(str(velocity))
				tn.write(" ")
				tn.write(str(GEAR))
				tn.write(" ")
				tn.write(str(CLUTCH))
				tn.write(" ")
				tn.write(str(BRAKE))
				tn.write(" ")
				tn.write(str(direction) + "\n")
			except:
				pass
		else:
			pass
		tn.close()
		ser.close()