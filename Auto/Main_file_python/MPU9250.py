#!/usr/bin/env python3

import smbus,time,sys
from math import sqrt, atan2, asin, degrees, radians, pi


bus = smbus.SMBus(1)

SLAVE_ADDRESS        = 0x68
AK8963_SLAVE_ADDRESS = 0x0C
DEVICE_ID            = 0x71

SMPLRT_DIV     = 0x19
CONFIG         = 0x1A
GYRO_CONFIG    = 0x1B
ACCEL_CONFIG   = 0x1C
ACCEL_CONFIG_2 = 0x1D
LP_ACCEL_ODR   = 0x1E
WOM_THR        = 0x1F
FIFO_EN        = 0x23
I2C_MST_CTRL   = 0x24
I2C_MST_STATUS = 0x36
INT_PIN_CFG    = 0x37
INT_ENABLE     = 0x38
INT_STATUS     = 0x3A
ACCEL_OUT      = 0x3B
TEMP_OUT       = 0x41
GYRO_OUT       = 0x43

I2C_MST_DELAY_CTRL = 0x67
SIGNAL_PATH_RESET  = 0x68
MOT_DETECT_CTRL    = 0x69
USER_CTRL          = 0x6A
PWR_MGMT_1         = 0x6B
PWR_MGMT_2         = 0x6C
FIFO_R_W           = 0x74
WHO_AM_I           = 0x75

GFS_250  = 0x00
GFS_500  = 0x01
GFS_1000 = 0x02
GFS_2000 = 0x03
AFS_2G   = 0x00
AFS_4G   = 0x01
AFS_8G   = 0x02
AFS_16G  = 0x03

AK8963_ST1        = 0x02
AK8963_MAGNET_OUT = 0x03
AK8963_CNTL1      = 0x0A
AK8963_CNTL2      = 0x0B
AK8963_ASAX       = 0x10

AK8963_MODE_DOWN   = 0x00
AK8963_MODE_ONE    = 0x01

AK8963_MODE_C8HZ   = 0x02
AK8963_MODE_C100HZ = 0x06

AK8963_BIT_14 = 0x00
AK8963_BIT_16 = 0x01

class MPU9250:

    declination = 0# Optional offset for true north. A +ve value adds to heading
    
    def __init__(self, address=SLAVE_ADDRESS):
        print("MPU Init...")
        self.address = address
        self.configMPU9250(GFS_250, AFS_2G)
        self.configAK8963(AK8963_MODE_C100HZ, AK8963_BIT_16)
        self.timestamp = 0
        self.GyroOff   = [0.115, -0.66, -0.272]        
        self.MagMaxMin = [[-152.904, 72.041, -71.015],
                         [-223.529, -2.987, -143.042]]

        self.MagBias   = [0.5*(self.MagMaxMin[0][0]+self.MagMaxMin[1][0]),
        				  0.5*(self.MagMaxMin[0][1]+self.MagMaxMin[1][1]),
        				  0.5*(self.MagMaxMin[0][2]+self.MagMaxMin[1][2])]
        
        MagDelta	   = [0.5*(self.MagMaxMin[0][0]-self.MagMaxMin[1][0]),
        				  0.5*(self.MagMaxMin[0][1]-self.MagMaxMin[1][1]),
        				  0.5*(self.MagMaxMin[0][2]-self.MagMaxMin[1][2])]
        MagAvg		   = (MagDelta[0]+MagDelta[1]+MagDelta[2])/3
        self.MagScale  = [MagAvg/MagDelta[0],
        				  MagAvg/MagDelta[1],
        				  MagAvg/MagDelta[2]]
        #self.MagBias   = [0,0,0]
        #self.MagScale  = [1,1,1]

        self.q = [1.0, 0.0, 0.0, 0.0]
        GyroMeasError = radians(40)
        self.beta = sqrt(3.0 / 4.0) * GyroMeasError 
        self.H = [0,0,0,0,0,0,0]#y,p,r,ycoe,dy,fy,Gyaw

    def searchDevice(self):
        who_am_i = bus.read_byte_data(self.address, WHO_AM_I)
        if(who_am_i == DEVICE_ID):
            return true
        else:
            return false

    def configMPU9250(self, gfs, afs):
        if gfs == GFS_250:
            self.gres = 250.0/32768.0
        elif gfs == GFS_500:
            self.gres = 500.0/32768.0
        elif gfs == GFS_1000:
            self.gres = 1000.0/32768.0
        else:
            self.gres = 2000.0/32768.0

        if afs == AFS_2G:
            self.ares = 2.0/32768.0
        elif afs == AFS_4G:
            self.ares = 4.0/32768.0
        elif afs == AFS_8G:
            self.ares = 8.0/32768.0
        else: 
            self.ares = 16.0/32768.0

        bus.write_byte_data(self.address, PWR_MGMT_1, 0x00)
        time.sleep(0.1)
        bus.write_byte_data(self.address, PWR_MGMT_1, 0x01)
        time.sleep(0.1)
        bus.write_byte_data(self.address, CONFIG, 0x03)
        bus.write_byte_data(self.address, SMPLRT_DIV, 0x04)
        bus.write_byte_data(self.address, GYRO_CONFIG, gfs << 3)
        bus.write_byte_data(self.address, ACCEL_CONFIG, afs << 3)
        bus.write_byte_data(self.address, ACCEL_CONFIG_2, 0x03)
        bus.write_byte_data(self.address, INT_PIN_CFG, 0x02)
        time.sleep(0.1)

    def configAK8963(self, mode, mfs):
        if mfs == AK8963_BIT_14:
            self.mres = 4912.0/8190.0
        else:
            self.mres = 4912.0/32760.0

        bus.write_byte_data(AK8963_SLAVE_ADDRESS, AK8963_CNTL1, 0x00)
        time.sleep(0.01)

        bus.write_byte_data(AK8963_SLAVE_ADDRESS, AK8963_CNTL1, 0x0F)
        time.sleep(0.01)

        data = bus.read_i2c_block_data(AK8963_SLAVE_ADDRESS, AK8963_ASAX, 3)

        self.magXcoef = (data[0] - 128) / 256.0 + 1.0
        self.magYcoef = (data[1] - 128) / 256.0 + 1.0
        self.magZcoef = (data[2] - 128) / 256.0 + 1.0

        bus.write_byte_data(AK8963_SLAVE_ADDRESS, AK8963_CNTL1, 0x00)
        time.sleep(0.01)

        bus.write_byte_data(AK8963_SLAVE_ADDRESS, AK8963_CNTL1, (mfs<<4|mode))
        time.sleep(0.01)

    def checkDataReady(self):
        drdy = bus.read_byte_data(self.address, INT_STATUS)
        if drdy & 0x01:
            return True
        else:
            return False

    def readAccel(self):
        data = bus.read_i2c_block_data(self.address, ACCEL_OUT, 6)
        x = self.dataConv(data[1], data[0])
        y = self.dataConv(data[3], data[2])
        z = self.dataConv(data[5], data[4])

        x = round(x*self.ares, 3)
        y = round(y*self.ares, 3)
        z = round(z*self.ares, 3)

        return {"x":x, "y":y, "z":z}

    def readGyro(self):
        data = bus.read_i2c_block_data(self.address, GYRO_OUT, 6)

        x = self.dataConv(data[1], data[0]) 
        y = self.dataConv(data[3], data[2])
        z = self.dataConv(data[5], data[4])

        x = round(x*self.gres, 3) - self.GyroOff[0]
        y = round(y*self.gres, 3) - self.GyroOff[1]
        z = round(z*self.gres, 3) - self.GyroOff[2]

        return {"x":x, "y":y, "z":z}

    def readMagnet(self):
        data = bus.read_i2c_block_data(AK8963_SLAVE_ADDRESS, AK8963_MAGNET_OUT, 7)

        x = self.dataConv(data[0], data[1])*self.mres*self.magXcoef
        y = self.dataConv(data[2], data[3])*self.mres*self.magYcoef
        z = self.dataConv(data[4], data[5])*self.mres*self.magZcoef

        x = (round(x, 3)-self.MagBias[0])*self.MagScale[0]
        y = (round(y, 3)-self.MagBias[1])*self.MagScale[1]
        z = (round(z, 3)-self.MagBias[2])*self.MagScale[2]

        return {"x":x, "y":y, "z":z}

    def readTemperature(self):
        data = bus.read_i2c_block_data(self.address, TEMP_OUT, 2)
        temp = self.dataConv(data[1], data[0])
        temp = round((temp / 333.87 + 21.0), 3)
        return temp

    def read(self,c = 0):
        data = bus.read_i2c_block_data(self.address, ACCEL_OUT, 6)

        ax = self.dataConv(data[1], data[0])*self.ares
        ay = self.dataConv(data[3], data[2])*self.ares
        az = self.dataConv(data[5], data[4])*self.ares

        data = bus.read_i2c_block_data(self.address, GYRO_OUT, 6)

        gx = self.dataConv(data[1], data[0])*self.gres-self.GyroOff[0]
        gy = self.dataConv(data[3], data[2])*self.gres-self.GyroOff[1]
        gz = self.dataConv(data[5], data[4])*self.gres-self.GyroOff[2]

        data = bus.read_i2c_block_data(AK8963_SLAVE_ADDRESS, AK8963_MAGNET_OUT, 7)

        mx = (self.dataConv(data[0],data[1])*self.magXcoef*self.mres\
        	 -self.MagBias[0])*self.MagScale[0]
        my = (self.dataConv(data[2],data[3])*self.magYcoef*self.mres\
        	 -self.MagBias[1])*self.MagScale[1]
        mz = (self.dataConv(data[4],data[5])*self.magZcoef*self.mres\
        	 -self.MagBias[2])*self.MagScale[2]

        tm = time(); 
        if self.timestamp !=0:
        	est = tm - self.timestamp
        	self.timestamp = tm
        else:
        	est = 0
        	self.timestamp = tm
        return {"ax":ax, "ay":ay, "az":az,
        		"gx":gx, "gy":gy, "gz":gz,
        		"mx":mx, "my":my, "mz":mz,
        		"et":est}

    def calibrate_Gyro(self):
    	print("Calib Gyro...")    	
    	self.GyroOff = [0,0,0]; GyroSet = [0,0,0]; ex = 1000
    	for i in range(0,ex):
    		data = self.readGyro()
    		GyroSet[0]+= data['x']
    		GyroSet[1]+= data['y']
    		GyroSet[2]+= data['z']
    	for i in range(0,3): GyroSet[i] = round(GyroSet[i]/ex,3)
    	self.GyroOff = GyroSet
    	return self.GyroOff

    def calibrate_Mag(self):
    	print("Calib Mag...")
    	self.MagMaxMin = [[0,0,0],[0,0,0]]
    	self.MagBias   = [0,0,0]
    	self.MagScale  = [1,1,1]
    	data = self.readMagnet()
    	MagMax = [data['x'],data['y'],data['z']]
    	MagMin = MagMax
    	try:
    		while 1:
    			data = self.readMagnet()
    			MagMax = [max(MagMax[0],data['x']),\
    					  max(MagMax[1],data['y']),\
    					  max(MagMax[2],data['z'])]
    			MagMin = [min(MagMin[0],data['x']),\
    					  min(MagMin[1],data['y']),\
    					  min(MagMin[2],data['z'])]
    			time.sleep(.01)
    			print(MagMax,MagMin)
    	except: pass
    	self.MagMaxMin = [MagMax,MagMin]
    	return(self.MagMaxMin)

    def YawOnly(self,x = 0):
    	data = bus.read_i2c_block_data(self.address, GYRO_OUT, 6)
    	Gz = round(self.dataConv(data[5], data[4])*self.gres,3)-self.GyroOff[2]
    	tm = time.time();
    	tp = -Gz*(tm-self.timestamp)
    	if self.timestamp !=0:
    		self.H[6]+= tp
    	else:
    		est = 0
    	self.timestamp = tm
    	erA = 45 if x-self.H[6]>45 else -45 if x-self.H[6]<-45 else x-self.H[6]
    	return self.H[6],erA,tp


    def fusion(self,c = 0):
        data = self.read()
        deltat = data['et']
        self.H[6] += deltat*data['gz']
        mx, my, mz = data['mx'],data['my'],data['mz']
        ax, ay, az = data['ax'],data['ay'],data['az']
        gx, gy, gz = radians(data['gx']),\
        			 radians(data['gy']),\
        			 -radians(data['gz'])
        q1, q2, q3, q4 = (self.q[x] for x in range(4))
        _2q1 = 2 * q1
        _2q2 = 2 * q2
        _2q3 = 2 * q3
        _2q4 = 2 * q4
        _2q1q3 = 2 * q1 * q3
        _2q3q4 = 2 * q3 * q4
        q1q1 = q1 * q1
        q1q2 = q1 * q2
        q1q3 = q1 * q3
        q1q4 = q1 * q4
        q2q2 = q2 * q2
        q2q3 = q2 * q3
        q2q4 = q2 * q4
        q3q3 = q3 * q3
        q3q4 = q3 * q4
        q4q4 = q4 * q4

        # Normalise accelerometer measurement
        norm = sqrt(ax * ax + ay * ay + az * az)
        if (norm == 0): return
        norm = 1 / norm
        ax *= norm
        ay *= norm
        az *= norm

        # Normalise magnetometer measurement
        norm = sqrt(mx * mx + my * my + mz * mz)
        if (norm == 0): return
        norm = 1 / norm            
        mx *= norm
        my *= norm
        mz *= norm

        # Reference direction of Earth's magnetic field
        _2q1mx = 2 * q1 * mx
        _2q1my = 2 * q1 * my
        _2q1mz = 2 * q1 * mz
        _2q2mx = 2 * q2 * mx
        hx = mx * q1q1 - _2q1my * q4 + _2q1mz * q3 + mx * q2q2 +\
             _2q2 * my * q3 + _2q2 * mz * q4 - mx * q3q3 - mx * q4q4
        hy = _2q1mx * q4 + my * q1q1 - _2q1mz * q2 + _2q2mx * q3 -\
        	 my * q2q2 + my * q3q3 + _2q3 * mz * q4 - my * q4q4
        _2bx = sqrt(hx * hx + hy * hy)
        _2bz = -_2q1mx * q3 + _2q1my * q2 + mz * q1q1 + _2q2mx * q4\
        	   - mz * q2q2 + _2q3 * my * q4 - mz * q3q3 + mz * q4q4
        _4bx = 2 * _2bx
        _4bz = 2 * _2bz

        # Gradient descent algorithm corrective step
        s1 = (-_2q3 * (2 * q2q4 - _2q1q3 - ax) + _2q2 * (2 * q1q2 + _2q3q4 - ay) - _2bz * q3 * (_2bx * (0.5 - q3q3 - q4q4)
             + _2bz * (q2q4 - q1q3) - mx) + (-_2bx * q4 + _2bz * q2) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my)
             + _2bx * q3 * (_2bx * (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz))

        s2 = (_2q4 * (2 * q2q4 - _2q1q3 - ax) + _2q1 * (2 * q1q2 + _2q3q4 - ay) - 4 * q2 * (1 - 2 * q2q2 - 2 * q3q3 - az)
             + _2bz * q4 * (_2bx * (0.5 - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx) + (_2bx * q3 + _2bz * q1) * (_2bx * (q2q3 - q1q4)
             + _2bz * (q1q2 + q3q4) - my) + (_2bx * q4 - _4bz * q2) * (_2bx * (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz))

        s3 = (-_2q1 * (2 * q2q4 - _2q1q3 - ax) + _2q4 * (2 * q1q2 + _2q3q4 - ay) - 4 * q3 * (1 - 2 * q2q2 - 2 * q3q3 - az)
             + (-_4bx * q3 - _2bz * q1) * (_2bx * (0.5 - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx)
             + (_2bx * q2 + _2bz * q4) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my)
             + (_2bx * q1 - _4bz * q3) * (_2bx * (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz))

        s4 = (_2q2 * (2 * q2q4 - _2q1q3 - ax) + _2q3 * (2 * q1q2 + _2q3q4 - ay) + (-_4bx * q4 + _2bz * q2) * (_2bx * (0.5 - q3q3 - q4q4)
              + _2bz * (q2q4 - q1q3) - mx) + (-_2bx * q1 + _2bz * q3) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my)
              + _2bx * q2 * (_2bx * (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz))

        norm = 1 / sqrt(s1 * s1 + s2 * s2 + s3 * s3 + s4 * s4) # normalise step magnitude
        s1 *= norm
        s2 *= norm
        s3 *= norm
        s4 *= norm

        # Compute rate of change of quaternion
        qDot1 = 0.5 * (-q2* gx - q3 * gy - q4 * gz) - self.beta * s1
        qDot2 = 0.5 * (q1 * gx + q3 * gz - q4 * gy) - self.beta * s2
        qDot3 = 0.5 * (q1 * gy - q2 * gz + q4 * gx) - self.beta * s3
        qDot4 = 0.5 * (q1 * gz + q2 * gy - q3 * gx) - self.beta * s4

        # Integrate to yield quaternion
        q1 += qDot1 * deltat
        q2 += qDot2 * deltat
        q3 += qDot3 * deltat
        q4 += qDot4 * deltat
        norm = 1 / sqrt(q1 * q1 + q2 * q2 + q3 * q3 + q4 * q4) # normalise quaternion
        self.q = q1 * norm, q2 * norm, q3 * norm, q4 * norm
        self.H[0] = self.declination + degrees(atan2(2.0 *\
        	(self.q[1] * self.q[2] + self.q[0] * self.q[3]),\
        	 self.q[0] * self.q[0] + self.q[1] * self.q[1] -\
        	 self.q[2] * self.q[2] - self.q[3] * self.q[3]))
        self.H[1] = degrees(-asin(2.0 * \
        	(self.q[1] * self.q[3] - self.q[0] * self.q[2])))
        self.H[2] = degrees(atan2(2.0 * \
        	(self.q[0] * self.q[1] + self.q[2] * self.q[3]),\
             self.q[0] * self.q[0] - self.q[1] * self.q[1] -\
             self.q[2] * self.q[2] + self.q[3] * self.q[3]))
        
        dh = self.H[0]-self.H[4]
        self.H[3]+= 1 if dh<-180 else -1 if dh>180 else 0
        self.H[5] = self.H[3]*360+self.H[0]        
        self.H[4] = self.H[0]
        return  self.H

    def dataConv(self, data1, data2):
        value = data1 | (data2 << 8)
        if(value & (1 << 16 - 1)):
            value -= (1<<16)
        return value



if __name__ == "__main__":
	try:
		mpu9250 = MPU9250()
		c = int(input("Check mode: "))
		if c == 0:			
			x = mpu9250.calibrate_Gyro()
			y = mpu9250.calibrate_Mag()
			print(x,y)
		while c == 1: 
			print(mpu9250.YawOnly())
		while c == 2:
			data = mpu9250.read()
			print(" ax = " , ( data['ax'] ))
			print(" ay = " , ( data['ay'] ))
			print(" az = " , ( data['az'] ))
			print(" gx = " , ( data['gx'] ))
			print(" gy = " , ( data['gy'] ))
			print(" gz = " , ( data['gz'] ))
			print(" mx = " , ( data['mx'] ))
			print(" my = " , ( data['my'] ))
			print(" mz = " , ( data['mz'] ))
			print(" et = " , ( data['et'] ))
			print(mpu9250.readTemperature())
			print()
			time.sleep(0.5)

	except KeyboardInterrupt:
		sys.exit()