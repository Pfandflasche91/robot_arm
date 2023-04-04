#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from time import time, sleep
from rupcom import Serial_com
from stepmotor import motor
from encoder import encoder
import threading

if __name__ == "__main__":
    starttime=time()
    ser=Serial_com()
    ser.open("/dev/ttyAMA0",56000)
    zmotor=motor(12, 16, 18, 22)
    zmotor.motorinit()
    zencoder=encoder(32)
    zencoder.ecoderInit()
    motorpositionalt=0
    #zmotor.move(20480,'cw')
    #time.sleep(4)
    #zmotor.motorStop()
    try:
       while True:
           #send='pos'+str(zmotor.position)+'\n'
           t=int(time()-starttime)/60#+(time()-starttime)%60*0.4
           print(t)
           if motorpositionalt != zmotor.position:
              print(t)   
              ser.write('pos'+str(zmotor.position)+'\n')
              ser.write('enc'+str(zencoder.getspeed())+'\n')
           #print(send)
           message=str(ser.read())
           print(message)
           if message[2]=='a':    
                zmotor.stop=False
                zmotor.move(2048,'cw')
           if message[2]=='b':
                zmotor.stop=False
                zmotor.move(2048,'ccw')
           if message[2]=='c':
               steps=message[3:7]
               print(steps)
               if steps != '     ':
                    zmotor.stop=False
                    zmotor.move(int(steps),'cw')
           if message[2]=='d':
               steps=message[3:7]
               print(steps)
               if steps != '     ':
                    zmotor.stop=False
                    zmotor.move(int(steps),'ccw')
                    #ser.write(str(zmotor.steps)+'\n')
           print(zencoder.getspeed())
           print(zmotor.position)
           print(zmotor.steps)
           #if zmotor.position >= 400:
               #zmotor.motorStop()
           motorpositionalt=zmotor.position 
           sleep(0.2)
           
    except KeyboardInterrupt:
        zmotor.motordeinit()
        ser.close()

