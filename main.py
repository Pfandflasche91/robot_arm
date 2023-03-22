#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
from rupcom import Serial_com

class motor():    
    def __init__(self,phaseA,phaseB,phaseC,phaseD):
        self.phaseA=phaseA
        self.phaseB=phaseB
        self.phaseC=phaseC
        self.phaseD=phaseD
        self.phase_state=8  #ABCD = 1000
    def motorinit(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.phaseA,GPIO.OUT)
        GPIO.setup(self.phaseB,GPIO.OUT)
        GPIO.setup(self.phaseC,GPIO.OUT)
        GPIO.setup(self.phaseD,GPIO.OUT)
        print("motorinit successfully")
    def motordeinit(self):
        GPIO.cleanup()
        print("motordeinit successfully")  
    def onestep(self,direction):
        if direction == 'cw':
            if self.phase_state==1:
                self.phase_state=8
            else:
                self.phase_state=self.phase_state >> 1
            if self.phase_state==1:
                GPIO.output(self.phaseA,GPIO.LOW)
                GPIO.output(self.phaseB,GPIO.LOW)
                GPIO.output(self.phaseC,GPIO.LOW)
                GPIO.output(self.phaseD,GPIO.HIGH)
            if self.phase_state==2:
                GPIO.output(self.phaseA,GPIO.LOW)
                GPIO.output(self.phaseB,GPIO.LOW)
                GPIO.output(self.phaseC,GPIO.HIGH)
                GPIO.output(self.phaseD,GPIO.LOW)
            if self.phase_state==4:
                GPIO.output(self.phaseA,GPIO.LOW)
                GPIO.output(self.phaseB,GPIO.HIGH)
                GPIO.output(self.phaseC,GPIO.LOW)
                GPIO.output(self.phaseD,GPIO.LOW)
            if self.phase_state==8:
                GPIO.output(self.phaseA,GPIO.HIGH)
                GPIO.output(self.phaseB,GPIO.LOW)
                GPIO.output(self.phaseC,GPIO.LOW)
                GPIO.output(self.phaseD,GPIO.LOW)

    def move(self,steps,direction):
        for i in range(steps):
            self.onestep(direction)
            time.sleep(0.003) 
            


def motorStop():
    for i in range(0,4,1):
        GPIO.output(motorPins[i],GPIO.LOW)

            

if __name__ == "__main__":
    ser=Serial_com()
    ser.open("/dev/ttyAMA0",9600)
    zmotor=motor(12, 16, 18, 22)
    zmotor.motorinit()
    try:
       while True:
           message=ser.read()
           print(message)
           #zmotor.move(2048,'cw')
           time.sleep(2)
           
    except KeyboardInterrupt:
        zmotor.motordeinit()
        ser.close()

