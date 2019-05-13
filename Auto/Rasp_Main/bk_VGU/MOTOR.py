#!/usr/bin/env python3

import RPi.GPIO as GPIO
import pigpio
import time

class MOTOR(object):
	"""docstring for MOTOR"""
	def __init__(self, x = 0):

		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.cleanup()

		self.pi = pigpio.pi()

		Mt = [20,21,12,16]#P1R,P2R,P1L,P2L
		En = [6 ,13,19,26]#AR, BR, AL, BL

		def encoderR(channel,lv,tick):
			self.SP[0]+=1
		def encoderL(channel,lv,tick):			
			self.SP[1]+=1

		GPIO.setup(Mt, GPIO.OUT)
		GPIO.setup(En, GPIO.IN)
		for i in range(4):
			self.pi.set_mode(Mt[i], pigpio.OUTPUT)
			self.pi.set_mode(En[i], pigpio.INPUT)

		self.MT = [0,0,0,0]
		self.SP = [0,0,0,0]

		self.pi.callback(En[0], pigpio.RISING_EDGE, encoderR)
		self.pi.callback(En[2], pigpio.RISING_EDGE, encoderL)
		'''
		GPIO.add_event_detect(En[0], GPIO.RISING, callback=encoder)
		GPIO.add_event_detect(En[2], GPIO.RISING, callback=encoder)
		'''
		for i in range(4):
			self.MT[i] = GPIO.PWM(Mt[i], 1000)
			self.MT[i].start(0)

	def run(self,R = 0, L = 0):
		R = 100 if R>100 else -100 if R<-100 else R
		L = 100 if L>100 else -100 if L<-100 else L
		if R>0:
			self.MT[0].ChangeDutyCycle(R)
			self.MT[1].ChangeDutyCycle(0)
		else:
			self.MT[0].ChangeDutyCycle(0)
			self.MT[1].ChangeDutyCycle(abs(R))
		if L>0:
			self.MT[2].ChangeDutyCycle(L)
			self.MT[3].ChangeDutyCycle(0)
		else:
			self.MT[2].ChangeDutyCycle(0)
			self.MT[3].ChangeDutyCycle(abs(L))

	def close(self):
		GPIO.cleanup()
		#MT.stop()

		

Motor = MOTOR()
for i in range(-100,100):
	print(Motor.SP[0],Motor.SP[1])
	Motor.run(i,-i)
	time.sleep(.05)


print(Motor.SP[0],Motor.SP[1])
time.sleep(.1)
print(Motor.SP[0],Motor.SP[1])
Motor.run(0,0)
#GPIO.setup(Mt, GPIO.OUT,initial=GPIO.LOW)
#GPIO.output(Mt[1], GPIO.HIGH)

