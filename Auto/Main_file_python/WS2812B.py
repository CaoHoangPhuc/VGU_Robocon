#!/usr/bin/env python3

import board
import neopixel
pixels = neopixel.NeoPixel(board.D18, 1)
from time import sleep
z,k,x,t = 5,0,0,0
erR,erL = 0,0
while 1:
	pixels[0] = (255,255,0) 
	sleep(.05)
	pixels[0] = (0,255,255) 
	sleep(.05)
	pixels[0] = (255,0,255) 
	sleep(.05)


x = 1
t = 0