#!/usr/bin/env python3

import board
import time
import neopixel
pixels = neopixel.NeoPixel(board.D18, 30)

while 1:

	pixels[0] = (0, 0, 255)
	time.sleep(1/100)
	pixels[0] = (255, 0, 0)

	time.sleep(1/100)
	pixels[0] = (0, 255, 0)

	time.sleep(1/100)
	pixels[0] = (255, 255, 255)
	time.sleep(1/100)
	pixels[0] = (0, 0, 0)
	time.sleep(1/100)