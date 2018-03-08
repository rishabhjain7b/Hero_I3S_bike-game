from serial import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)

while 1:
	serial_line = ser.readline()
	print(serial_line)
	time.sleep(2)
ser.close()
