########################################################################################
#Project: Hero Bike Project version 1.0
#Info: Customised solution for Hero i3S Motorbike simulator
#Team: Shreyas & Arpit
#Date of Completion: 22 MAY 2014
#P.S.: 1. IR sensor module for Speed Calculation (KM/Hr)
#	   2. Induced Proximity sensor for Left Handle Orientation (NPN) and Right Handle Orientation (NPN)
#	   3. Physically RIGHT Proximity sensor is logically working for LEFT side and vice versa.
#	   4. Internal connections for i3S and Brake input from Bike
########################################################################################

import RPi.GPIO as GPIO
import time
import telnetlib
import sys
import math


GPIO.setmode(GPIO.BCM)
tn = telnetlib.Telnet("169.254.178.66","1080")

PRO_LEFT_LOG_RIGHT = 23
PRO_RIGHT_LOG_LEFT = 24
i3S_ON_PIN = 9
i3S_OFF_PIN = 10
Brake_PIN = 11
Sensor_PIN = 25

BRAKE = 0
i3S = 0
direction = 0
xm=0
xdiff= 0
xm_old= -1
tm=0
tdiff=0
tm_old= -1
counter= 0
velocity = 0
temp=0
counter_stop=0
flag = 0
xm_1 = 0
P_value = 9999

GPIO.setup(PRO_LEFT_LOG_RIGHT, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(PRO_RIGHT_LOG_LEFT, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(i3S_ON_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(i3S_OFF_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(Brake_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(Sensor_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

try:
	print "Ready"
	xm = time.time()

	while True:
		while GPIO.input(Sensor_PIN) == False:
			xm_1 = time.time()
			xdiff = (xm_1 - xm)
			if(xdiff < 0 or xdiff >1):
				velocity = 0

			if GPIO.input(PRO_LEFT_LOG_RIGHT) == False and GPIO.input(PRO_RIGHT_LOG_LEFT) == True:
				direction = 0      		#left													#LEFT sensor is ACTIVE HIGH, RIGHT sensor is ACTIVE HIGH

			if GPIO.input(PRO_LEFT_LOG_RIGHT) == True and GPIO.input(PRO_RIGHT_LOG_LEFT) == False:
				direction = 2			#right

			if GPIO.input(PRO_LEFT_LOG_RIGHT) == False and GPIO.input(PRO_RIGHT_LOG_LEFT) == False:
				direction = 1			#centre


			if GPIO.input(Brake_PIN) == True:
				BRAKE = 1					#Brake_ON

			else:
				BRAKE = 0					#Brake_OFF


			if GPIO.input(i3S_ON_PIN) == True:
				i3S = 1						#i3S_ON

			if GPIO.input(i3S_OFF_PIN) == False:
				i3S = 0						#i3S_OFF

			all_value =(1000*velocity)+(100*BRAKE)+(10*direction)+i3S
			if all_value != P_value:
				P_value = all_value
				print velocity,""+str(BRAKE),""+str(direction),""+str(i3S)
			#	tn.write(str(velocity))
			#	tn.write(" ")
			#	tn.write(str(BRAKE))
			#	tn.write(" ")
			#	tn.write(str(direction))
			#	tn.write(" ")
			#	tn.write(str(i3S) + "\n")#tn.write(str(BRAKE))



		xm = time.time()



		if GPIO.input(Sensor_PIN) == True:
			while GPIO.input(Sensor_PIN) == True:
				pass

			counter += 1

			tm = time.time()
			tdiff = (tm - tm_old) if tm_old > 0  else  0
			tm_old = tm
			if(counter == 2):
				counter= 0

				temp=math.ceil(3.14/tdiff)			# R = 34.5cm = 0.345m, So 2pi*r = 0.2198
				velocity= int(temp)

		if GPIO.input(PRO_LEFT_LOG_RIGHT) == False and GPIO.input(PRO_RIGHT_LOG_LEFT) == True:
			direction = 0      		#left													#LEFT sensor is ACTIVE HIGH, RIGHT sensor is ACTIVE HIGH

		if GPIO.input(PRO_LEFT_LOG_RIGHT) == True and GPIO.input(PRO_RIGHT_LOG_LEFT) == False:
			direction = 2			#right

		if GPIO.input(PRO_LEFT_LOG_RIGHT) == False and GPIO.input(PRO_RIGHT_LOG_LEFT) == False:
			direction = 1			#centre


		if GPIO.input(Brake_PIN) == True:
			BRAKE = 1					#Brake_ON

		else:
			BRAKE = 0					#Brake_OFF


		if GPIO.input(i3S_ON_PIN) == True:
			i3S = 1						#i3S_ON

		if GPIO.input(i3S_OFF_PIN) == False:
			i3S = 0						#i3S_OFF

		#print str(i3S) + str(BRAKE) + str(direction) + str(velocity)
		all_value =(1000*velocity)+(100*BRAKE)+(10*direction)+i3S
		if all_value != P_value:
			P_value = all_value
			print velocity,""+str(BRAKE),""+str(direction),""+str(i3S)
		#	tn.write(str(velocity))
		#	tn.write(" ")
		##	tn.write(str(BRAKE))
		#	tn.write(" ")
		#	tn.write(str(direction))
		#	tn.write(" ")
		#	tn.write(str(i3S) + "\n")#tn.write(str(BRAKE))

except KeyboardInterrupt:

               print "Quit"

               GPIO.cleanup()
