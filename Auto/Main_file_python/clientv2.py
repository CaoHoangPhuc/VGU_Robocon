#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## Khai báo các thư viện được sử dụng
import websocket
import json
import ssl
import time
import urllib.request
from pathlib import Path
#import dataProcessing as AS


## Cài đặt và trả về thông tin cho giao thức mã hoá HTTPS
def makeSSLContext(ca, crt, key):
    sslCTX = ssl.create_default_context(
        purpose=ssl.Purpose.SERVER_AUTH,
        cafile=ca
    )

    sslCTX.load_cert_chain(crt, key)

    return sslCTX


## Trả về chuỗi JSON chứa thông tin đăng nhâp
def makeJSONCredentials(username, password):
    creds = {
        "username": username,
        "password": password
    }

    return json.dumps(creds).encode("utf-8")


## Cài đặt và trả về thông tin của yêu cầu HTTPS
def makeRequestHeader(url, contentType, content):
    req = urllib.request.Request(url)

    req.add_header('Content-Type', contentType)
    req.add_header('Content-Length', len(content))

    return req


## Gửi yêu cầu đăng nhập và trả về mã xác thực
def getToken(url, username, password,
             ca, crt, key):
    reqSSLContext = makeSSLContext(ca, crt, key)
    reqContent = makeJSONCredentials(username, password)
    req = makeRequestHeader(
        url,
        'application/json; charset=utf-8',
        reqContent
    )

    # Gửi yêu cầu và nhận kết quả trả về
    resp = urllib.request.urlopen(
        req, data=reqContent, context=reqSSLContext)

    # Đọc và trả về mã xác thực
    respBody = resp.read()
    respBodyJSON = json.loads(respBody.decode('utf-8'))

    return respBodyJSON["token"]


# Đăng nhập và nhận dữ liệu


## Cài đặt thông tin của giao thức mã hoá cho Websocket

# Đường dẫn đến các tập tin nhận từ BTC
CA_CRT = str(Path("cacert_TDT.pem"))
CRT = str(Path("clientcert_TDT.pem"))
KEY = str(Path("clientkey_TDT.pem"))

sslopt = {
    'cert_reqs': ssl.PROTOCOL_SSLv23,
    'keyfile': KEY,
    'certfile': CRT,
    'ca_certs': CA_CRT,
}


## Nhận mã xác thực và thêm mã xác thực vào thông tin yêu cầu Websocket

# Tên địa chỉ server (thay đổi vào ngày thi đấu)
HOST = "192.168.1.100"
#HOST = "test.tunglevo.com"
# Tên cổng kết nối (thay đổi vào ngày thi đấu)
PORT = 4433

url = 'https://%s:%s/subscribe' % (HOST, PORT)
token = getToken(url,
                 # Thông tin tài khoản của mỗi đội
                 'TDTU', '4uGWWUCb',
                 CA_CRT, CRT, KEY)

header = {
    'Authorization': 'Bearer %s' % (token)
}

sslopt = {
    'cert_reqs': ssl.PROTOCOL_SSLv23,
    'keyfile': KEY,
    'certfile': CRT,
    'ca_certs': CA_CRT,
}

## Thiết lập kết nối Websocket và bắt đầu nhận dữ liệu
url = 'wss://%s:%s/data' % (HOST, PORT)
ws = websocket.create_connection(url,
                                 header=header,
                                 sslopt=sslopt)

#Connect to Bluetooth
#AS.serconnect()



import numpy as np
import matplotlib.pyplot as plt
from math import tan,pi,atan2,cos,sin,radians,degrees

from MOTOR import MOTOR
from MPU9250 import MPU9250

Motor = MOTOR()
Mpu9250 = MPU9250()
#18,19,20,21 [M1,M2,A1,A2]
Tar = 19
Con = 20
lh = 0
cofh=0
le = 0
cofe=0
def dist(x,y,z):
    global lh,cofh,le,cofe
    a = round(pow((y[0]-x[0])**2+(y[1]-x[1])**2,0.5),1)
    b = round(degrees(atan2(y[1]-x[1],y[0]-x[0])),1)
    if lh ==0: lh =b
    cofh +=-1 if b - lh >180 else 1 if b - lh <-180 else 0
    lh = b
    c = round(degrees(atan2(z[1],z[0])),1)
    if le ==0: le =c
    cofe +=-1 if c - le >180 else 1 if c - le <-180 else 0
    le = c

    return a,b,c

def run(x,sp,dst):
    x = 70 if x>70 else -70 if x <-70 else x
    if abs(x)>35:Motor.run(x,-x)
    else: Motor.run(sp+x,sp-x)
    print(x)
msg = ws.recv()
packet = json.loads(msg.decode('utf-8'))
data = dist(packet['data'][Con]['position'],\
        packet['data'][Tar]['position'],packet['data'][Con]['dimension'])
ws.send(json.dumps({'finished': True}).encode('utf-8'))

DIRECTION = 0
HEADING = 0
while True:
    msg = ws.recv()
    packet = json.loads(msg.decode('utf-8'))
    print(packet['data'][Tar])
    print(packet['data'][Con]) 
    if int(packet['data'][Con]['position'][0])>0 and\
        int(packet['data'][Tar]['position'][0])>0:
        data = dist(packet['data'][Con]['position'],\
        packet['data'][Tar]['position'],packet['data'][Con]['dimension'])
        DIRECTION= (data[1]+cofh*360)
        HEADING = (data[2]+cofe*360)
        run(0.3*(HEADING-DIRECTION),70,data[0])

    ws.send(json.dumps({'finished': True}).encode('utf-8'))

    
    #previousDistance = AS.main(packet, previousDistance)
    