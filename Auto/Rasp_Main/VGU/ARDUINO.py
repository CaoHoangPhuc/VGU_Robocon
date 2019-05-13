#!/usr/bin/env python3

import smbus
import RPi.GPIO as GPIO
import time
import sys

bus = smbus.SMBus(1)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class ARDUINO(object):
    """docstring for Arduino"""
    def __init__(self,address = 0x04):
        print("Arduino init..")
        self.add = address 
        bat = self.Bat()
        for i in range(-100,101,10):
            self.Motor(i,-i,90)
            time.sleep(.1)
        self.Motor(0,0,90)
        print("Arduino ok! Bat = ",bat)

    def mapf(self,val,inmin,inmax,outmin,outmax):
        return (val-inmin)*(outmax-outmin)/(inmax-inmin)+outmin

    def readdata(self,bit = 2, off = 0):
        temp = [0,0] 
        try: temp = bus.read_i2c_block_data(self.add, off, bit)
        except IOError: temp = [0,0]
        return temp[0]*256+temp[1]

    def writedata(self,data, off = 0):
        try:bus.write_i2c_block_data(self.add, off, data)
        except IOError: pass

    def Bat(self):
        try: temp = self.readdata(2)
        except IOError: temp = -1
        return self.mapf(temp,0,1024,0,16)

    def Motor(self,MR,ML,SV=90, c = 0):
        byte = [0 if MR<0 else 1, abs(int(MR)),
                0 if ML<0 else 1, abs(int(ML)),
                int(SV)]
        try: self.writedata(byte)
        except IOError: c = -1
        return c

    def exit(self):
        self.Motor(0,0)
        print("Bat = ",self.Bat())
        

if __name__ == "__main__":
    Arduino = ARDUINO(0x04) 
    try:            
        c = int(input("Check mode: "))
        while c == 0:
            bat = Arduino.Bat()
            print(bat)
            time.sleep(.1)
        while c == 1: 
            x = input("Motor(R,L,S)= ")
            x = [int(z) for z in x.split()]
            Arduino.Motor(x[0],x[1],x[2])

    except KeyboardInterrupt:
        Arduino.exit()
        sys.exit()