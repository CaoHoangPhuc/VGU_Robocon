#!/usr/bin/env python3

import RPi.GPIO as GPIO
import numpy as np
import time
from MPU9250 import MPU9250
from ARDUINO import ARDUINO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

Arduino = ARDUINO()
Mpu9250 = MPU9250()

def Main():	
	while 1:
		print(Mpu9250.fusion())


Main()