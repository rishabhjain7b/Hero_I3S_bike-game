import time
import serial

ser = serial.Serial('/dev/ttyAMA0', 115200)

while 1:
	serial_line = ser.readline()
	value = serial_line
	print(value)
	time.sleep(0.2)
ser.close()
