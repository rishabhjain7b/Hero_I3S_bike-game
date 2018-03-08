import socket
import time
import sys
import os
#from socket import *
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
Relay_PIN = 4
GPIO.setup(Relay_PIN, GPIO.OUT)

HOST = ''
PORT = 1818

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#serversocket = socket()
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((HOST, PORT))
serversocket.listen(10)
GPIO.output(Relay_PIN, GPIO.HIGH)

while 1:
	connection, address = serversocket.accept()
	data = connection.recv(1024)

	if "E0" in data:
		GPIO.output(Relay_PIN, GPIO.HIGH)
	
	if "E1" in data:
		GPIO.output(Relay_PIN, GPIO.LOW)
	
	data = None
#serversocket.shutdown(1)
serversocket.close()
