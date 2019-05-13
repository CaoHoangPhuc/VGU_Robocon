#!/usr/bin/env python3

import time
import serial
import threading

ser = serial.Serial(
	port='/dev/ttyS0', 
	baudrate = 115200,
	timeout=1
)
counter=0

def Motor(R,L):
	st = str(R+500)+";"+str(L+500);
	return st

def f():
	ser.write(Motor(0,0).encode())
	threading.Timer(.1, f).start()

threading.Timer(1.0, f).start()




while 1:
	while ser.inWaiting()>0:		
		print(ser.readline())
	counter += 1

