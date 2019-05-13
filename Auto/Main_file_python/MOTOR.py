#!/usr/bin/env python3

import RPi.GPIO as GPIO
from time import time,sleep
from threading import Timer

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup()

class MOTOR(object):
	"""docstring for MOTOR"""
	def __init__(self, x = 0):

		self.Mt = [7,12,16,20]#P1R,P2R,P1L,P2L #change 21
		'''
		self.En = [26,19,6 ,13]#AR, BR, AL, BL

		self.PIDR=[.1,.2,.05,0 ,0 ,0]#kp,ki,kd,I,lD,Out
		self.PIDL=[.1,.2,.05,0 ,0 ,0]#kp,ki,kd,I,lD,Out
		self.dt = 0

		if x==1:
			def enR(channel):
				self.SP[0]+= self.SP[4]
			def enL(channel):
				self.SP[1]+= self.SP[5]
		else:
			def enR(channel):
				if abs(self.SP[6])>500:
					self.SP[0]+= self.SP[4]
					self.SP[6] = 0.9*self.SP[6]+0.1*self.SP[4]/(time()-self.SP[8])
				else:
					tp1 =-(GPIO.input(self.En[1])*2-1)
					self.SP[0]+= tp1
					self.SP[6] = 0.9*self.SP[6]+0.1*tp1/(time()-self.SP[8])
				self.SP[8] = time()
			def enL(channel):
				if abs(self.SP[7])>500:
					self.SP[1]+= self.SP[5]
					self.SP[7] = 0.9*self.SP[7]+0.1*self.SP[5]/(time()-self.SP[9])
				else:
					tp1 = GPIO.input(self.En[3])*2-1
					self.SP[1]+= tp1
					self.SP[7] = 0.9*self.SP[7]+0.1*tp1/(time()-self.SP[9])
				self.SP[9] = time()
		'''
		GPIO.setup(self.Mt, GPIO.OUT,initial = GPIO.LOW)
		'''
		GPIO.setup(self.En, GPIO.IN)

		
		self.SP = [0,0,0,0,0,0,0,0,time(),time(),0,0]
		self.Spd= [0,0]
		GPIO.add_event_detect(self.En[0], GPIO.RISING, callback=enR)
		GPIO.add_event_detect(self.En[2], GPIO.RISING, callback=enL)
		'''
		self.MT = [0,0]
		self.MT[0] = GPIO.PWM(self.Mt[0], 1000)
		self.MT[1] = GPIO.PWM(self.Mt[2], 1000)
		self.MT[0].start(0)
		self.MT[1].start(0)

		#self.calculateSP()


	def calculateSP(self):
		t = time()
		if self.dt !=0:
			self.SP[2] = 0.9*self.SP[2]+0.1*(self.SP[0]-self.SP[10])/(t-self.dt)
			self.SP[3] = 0.9*self.SP[3]+0.1*(self.SP[1]-self.SP[11])/(t-self.dt)
		self.dt = t
		self.SP[10:12] = self.SP[0:2]
		Timer(.01,self.calculateSP).start()

	def Speed(self):
		R= 0.9*self.SP[2]+0.1*self.SP[6]
		L= 0.9*self.SP[3]+0.1*self.SP[7]
		return R,L

	def run(self,R = 0, L = 0):
		R = 100 if R>100 else -100 if R<-100 else R
		L = 100 if L>100 else -100 if L<-100 else L
		'''
		self.SP[4]=1 if R>0 else -1 if R<0 else 0
		self.SP[5]=1 if L>0 else -1 if L<0 else 0
		'''
		if R>=0:
			self.MT[0].ChangeDutyCycle(R)
			GPIO.output(self.Mt[1], GPIO.LOW)
		else:
			self.MT[0].ChangeDutyCycle(100-abs(R))
			GPIO.output(self.Mt[1], GPIO.HIGH)
		if L>=0:
			self.MT[1].ChangeDutyCycle(L)
			GPIO.output(self.Mt[3], GPIO.LOW)
		else:
			self.MT[1].ChangeDutyCycle(100-abs(L))
			GPIO.output(self.Mt[3], GPIO.HIGH)
	'''
	def PID(self,R = 0,L = 0):	
		erR,erL = self.Speed()
		erR = R - erR
		erL = L - erL

		self.PIDR[3]+= self.PIDR[1]*erR*.01
		self.PIDL[3]+= self.PIDL[1]*erL*.01

		self.PIDR[3] = 100 if self.PIDR[3]> 100 else\
					  -100 if self.PIDR[3]<-100 else self.PIDR[3]
		self.PIDL[3] = 100 if self.PIDL[3]> 100 else\
					  -100 if self.PIDL[3]<-100 else self.PIDL[3]

		dR = self.PIDR[2]*(erR-self.PIDR[4])
		dL = self.PIDL[2]*(erL-self.PIDL[4])

		self.PIDR[4] = erR
		self.PIDL[4] = erL

		self.PIDR[5] = self.PIDR[0]*erR+self.PIDR[3]+dR
		self.PIDL[5] = self.PIDL[0]*erL+self.PIDL[3]+dL

		self.run(self.PIDR[5],self.PIDL[5])
	'''
	def close(self):		
		self.run(0,0)
		#GPIO.remove_event_detect(self.En[0])
		#GPIO.remove_event_detect(self.En[2])
		for i in range(2): self.MT[i].stop()	
		GPIO.cleanup()

		

if __name__ == "__main__":
	#from MPU9250 import MPU9250
	import board
	import neopixel
	try:
		Motor = MOTOR()
		#Mpu9250= MPU9250()
		while 1:
			x = input("nhap = : ")
			if x == 'w':Motor.run(20,20)
			if x == 's':Motor.run(-20,-20)
			if x == 'a':Motor.run(20,-20)
			if x == 'f':Motor.run(0,0)
			if x == 'd':Motor.run(-20,20)
			if x == 'q':Motor.run(20,20)
			if x == 'e':Motor.run(20,50)
			if x == 'z':Motor.run(100,100)
			if x == 'x':Motor.run(0,20)
			if x == 'c':Motor.run(0,-20)
			if x == 'v':Motor.run(-20,0)
			sleep(0.2)
			#Motor.run(50,50)
		
		x = 90
		while 1:
			#z = Mpu9250.YawOnly(x)
			#Motor.PID(500+z[1]*10,500-z[1]*10)
			Motor.run(50+z[1],50-z[1])
			#print(Motor.PIDR)
			#Motor.PID(200,200)
			print(z)
			sleep(.01)
			if abs(z[1])<1: x+=x
		z = 0
		k = 0

		#pixels = neopixel.NeoPixel(board.D18, 1)
		while 0:
			erR,erL = Motor.Speed()
			if k>=255: z = -5
			if k<=0: z = 5
			k+=z
			t = 255 if erR>=0 else 0
			x = 255 if erL>=0 else 0
			pixels[0] = (int(t*(1-k/255)),int(x*(1-k/255)),k) 
			sleep(.01)
		
	except KeyboardInterrupt:
		Motor.close()
		exit()