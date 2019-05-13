import numpy as np
import matplotlib.pyplot as plt
from time import time,sleep
from math import tan,pi,atan2,cos,sin,radians,degrees
#from MOTOR import MOTOR
#from MPU9250 import MPU9250

#Motor = MOTOR()
#Mpu9250= MPU9250()

ObjCha = [['object_1',  'hop',  5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['object_2',  'hop',  5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['object_3',  'hop',  5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['object_4',  'hop',  5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['object_5',  'hop',  5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['object_6',  'hop',  5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['object_7',  'hop',  5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['object_8',  'det', 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['object_9',  'det', 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['object_10', 'det', 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['object_11', 'det', 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['object_12', 'dia', 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['object_13', 'dia', 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['object_14', 'dia', 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['object_15', 'bay', 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['object_16', 'bay', 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['object_17', 'ban', 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['object_18', 'ban', 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['object_19', 'phi', 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['object_20', 'phi', 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['object_21', 'bom', 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['object_22', '---',  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['object_23', '---',  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['object_24', '---',  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['auto_1',     'a1', -5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['auto_2',     'a2',-10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['manual_1',   'm1',-15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		  ['manual_2',   'm2',-20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

autoindex =  ['auto_1',1]
manual_ally =['manual_1',2]
auto_foe =   ['auto_2',3]
manual_foe = ['manual_2',4]

ObjCha = np.array(ObjCha,dtype = object)
#0name,1obj,2score,3xpos,4ypos,5xdim,6ydim,7dis,8dir,9head
#10coedir,#11Ldir,#12coedir,#13Lhead,#14v,#15forwardAngle,#16omega#17ld
'''
BatGnd = np.ones((302,302),dtype = int)*50

Zone1  = np.array([1,110,51,190,1])
Zone2  = np.array([249,111,299,191,2])
Bar1   = np.array([1,190,51,191,50])
Bar2   = np.array([249,110,299,111,50])
PlayGd = np.array([1,1,299,299,0])

Path   = np.ones((300,300),dtype = int)*9999

A1 = [50,50,48]
Ob = [150,150,49]
'''
def fill(data,area):
	for x in area:
		for i in range(x[0],x[2]):
			for j in range(x[1],x[3]):
				data[i][j]=x[4]
def point(data,pt):
	for x in pt:
		data[x[0]][x[1]]=x[2]

def cnode(data,i,j):
	if BatGnd[i][j]<3:
		data[i][j] = 1+min(data[i][j-1],data[i][j+1],
			data[i-1][j-1],data[i-1][j],data[i-1][j+1],
			data[i+1][j-1],data[i+1][j],data[i+1][j+1])

def pathf(data,s,g):
	Path[g[0]][g[1]] = 0
	t = time()
	def update(data):
		r = np.array(data.shape)-1
		for i in range(0,r[0]):
			for j in range(0,r[1]):
				cnode(data,i,j)
				cnode(data,i,r[1]-j)
				cnode(data,r[0]-i,j)
				cnode(data,r[0]-i,r[1]-j)
		
	update(Path)
	print(time()-t)
	print(BatGnd[g[0]])
	print(Path[200])
def Pre(data):
	fill(BatGnd,[PlayGd,Zone1,Zone2,Bar1,Bar2])
	point(data,[A1,Ob])
	pathf(data,A1,Ob)



def sort(data,index = 2):
	def ex(data,i,j):
		x = np.array(data[i])
		data[i] = data[j]
		data[j] = x
	for i in range(len(data)):
		for j in range(len(data)-1):
			if int(data[j][index])<int(data[j+1][index]): 				
				ex(data,j,j+1)

def dist(x,y,z):	
	d = round(pow((y[0]-x[0])**2+(y[1]-x[1])**2,0.5),1)
	c = round(degrees(atan2(y[1]-x[1],y[0]-x[0])),1)
	h = round(degrees(atan2(z[1],z[0])),1)
	#h = 0.9*(h + Mpu9250.YawOnly()[3]) + 0.1*h
	return d,c,h

def exdata(x,y):
	x[0] = y[0]-y[3]
	x[1]+= -1 if y[1]-y[4]>180 else 1 if y[1]-y[4]<-180 else 0
	x[2]+= -1 if y[2]-y[5]>180 else 1 if y[2]-y[5]<-180 else 0
	return x

def preprocess(packet):
	x = packet['time']
	for i in packet["data"]:
		index = np.where(ObjCha == i['name'])[0][0]
		#print(np.where(ObjCha == i['name']))
		if (i['position'][0] == -1) and (i['position'][1] == -1):
			ObjCha[index][2] = 0
		ObjCha[index][3:7]= [*np.array(i['position']),*np.array(i['dimension'])]
	
	'''
	ObjCha[24][3:7] = np.array([148.2, 147.2, -27, -88])
	ObjCha[25][3:7] = np.array([138.2, 140.2, -71, -83])
	ObjCha[26][3:7] = np.array([298.6, 183.0, -68, -49])
	ObjCha[27][3:7] = np.array([99.8, 238.2, -54, 14])
	'''
	
def preprocess2(packet):
	pass
	

def calculate(agent):
	index  = agent[1]
	x = ObjCha[index][3:5]
	for i in range(len(ObjCha)):
		y = ObjCha[i][3:5]
		z = ObjCha[i][5:7]
		ObjCha[i][10:13]= ObjCha[i][7:10]
		ObjCha[i][7:10] = dist(x,y,z)
		if (ObjCha[i][10:13]==[0,0,0]).all() :ObjCha[i][7:10]
		ObjCha[i][13:16]= exdata(ObjCha[i][13:16],ObjCha[i][7:13])


def play(pick):
	#print(ObjCha[24,3:])
	print(ObjCha[pick,8:])
	#calculate(autoindex)	
	def rotate(w):
		#ObjCha[autoindex[1]][9]+=round(0.3*w,1)
		#ObjCha[autoindex[1]][5]=85*cos(radians(ObjCha[autoindex[1]][9]+0.3*w))
		#ObjCha[autoindex[1]][6]=85*sin(radians(ObjCha[autoindex[1]][9]+0.3*w))
		#ObjCha[24][9]+ObjCha[24][15]*360
		w = 20 if w >20 else -20 if w<-20 else w
		#Motor.run(w,-w)
		print('r',0.3*w)
		pass
	def go():
		#ObjCha[autoindex[1]][3]+=round(2*cos(radians(ObjCha[autoindex[1]][9])),1)
		#ObjCha[autoindex[1]][4]+=round(2*sin(radians(ObjCha[autoindex[1]][9])),1)
		#Motor.run(30,30)
		#print('m')
		pass
	def move(foe):
		head = (ObjCha[foe][8]+ObjCha[foe][14]*360)\
				-(ObjCha[24][9]+ObjCha[24][15]*360)
		#print(ObjCha[foe][8])
		#Motor.PID(500+head*10,500-head*10)
		if abs(head)>5:rotate(head)
		else: go()


	def pl():
		for i in ObjCha[0:28]:
			plt.plot(i[3],i[4],'ro')
			plt.text(i[3],i[4], i[0], fontsize=8)
			if i[0]!=autoindex[0]:
				for j in range(0,20):
					plt.plot(ObjCha[autoindex[1]][3]+j*cos(radians(i[8])),\
						ObjCha[autoindex[1]][4]+j*sin(radians(i[8])),'g.')
			else:
				for j in range(0,30):
					plt.plot(i[3]+j*cos(radians(i[9])),i[4]+j*sin(radians(i[9])),'b.')
	
	'''
	pl()
	plt.show(block = 0)
	plt.pause(.01)
	plt.clf()
	'''
	
	#z = Mpu9250.YawOnly(ObjCha[pick][8])
	#Motor.PID(500+z[1]*10,500-z[1]*10)
	move(pick)
	#rotate(-10)
	#play(pick)

Tar = 15
Con = 18
Lt = np.array([[0,0],[0,0]])
Lc = np.array([[0,0],[0,0]])
x = 0
def main(data):
	global Lt,Lc
	#preprocess(data)
	print(data['data'][Tar])
	print(data['data'][Con])
	Tarx = np.array([data['data'][Tar]['position'],data['data'][Tar]['dimension']])
	Conx = np.array([data['data'][Con]['position'],data['data'][Con]['dimension']])
	if np.sum(Tarx)<=0: Tarx = Lt
	if np.sum(Conx)<=0: Conx = Lc

	d,h,c = dist(Tarx[0],Conx[1],Conx[1])
	print(d,h,c)

	Lt = Tarx
	Lc = Conx
	#calculate(autoindex)
	#Motor.run(-0.1*h,0.1*h)
	#sort(ObjCha)
	#print(ObjCha[24:])
	#plt.axis([0, 300, 0, 300])
	#pick = 0
	try:
		pass
	except KeyboardInterrupt:
		Motor.close()
		exit()
	#print(ObjCha)

if __name__ == "__main__":
	pass
	#Pre(BatGnd)
	#plt.imshow(200-Path, cmap="gray",vmin=0,vmax=200,aspect='auto')
	#plt.imshow(50-BatGnd, cmap="gray",vmin=0,vmax=50,aspect='auto')
	#plt.show()