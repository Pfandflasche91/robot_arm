#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from rupcom import Serial_com
from stepmotor import motor
from encoder import encoder
import threading

if __name__ == "__main__":
    ser=Serial_com()
    ser.open("/dev/ttyAMA0",9600)
    zmotor=motor(12, 16, 18, 22)
    zmotor.motorinit()
    zencoder=encoder(32)
    zencoder.ecoderInit()
    #zmotor.move(20480,'cw')
    #time.sleep(4)
    #zmotor.motorStop()
    try:
       while True:
           ser.write(str(zmotor.steps)+'\n')
           message=str(ser.read())
           #print(message)
           if message[2]=='a':    
                zmotor.stop=False
                zmotor.move(2048,'cw')
           if message[2]=='b':
                zmotor.stop=False
                zmotor.move(2048,'ccw')
           if message[2]=='c':
               steps=message[3]+message[4]+message[5]+message[6]+message[7]
               print(steps)
               if steps != '     ':
                    zmotor.stop=False
                    zmotor.move(int(steps),'cw')
           if message[2]=='d':
               steps=message[3]+message[4]+message[5]+message[6]+message[7]
               print(steps)
               if steps != '     ':
                    zmotor.stop=False
                    zmotor.move(int(steps),'ccw')
                    ser.write(str(zmotor.steps)+'\n')
           print(zencoder.getspeed())
           #print(zmotor.position)
           #if zmotor.position >= 400:
               #zmotor.motorStop()
            
           time.sleep(1)
           
    except KeyboardInterrupt:
        zmotor.motordeinit()
        ser.close()

