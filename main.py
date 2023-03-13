#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from serial import Serial
import time

ser=Serial("/dev/ttyAMA0")
ser.baudrate=9600


motorPins = (12, 16, 18, 22) #define pins connected   
CCWStep = (0x01,0x02,0x04,0x08) #define power supply order for coil for rotating anticlockwise 
CWStep = (0x08,0x04,0x02,0x01)  #define power supply order for coil for rotating clockwise
 
def motorinit():
    GPIO.setmode(GPIO.BOARD)
    for pin in motorPins:
        GPIO.setup(pin,GPIO.OUT)
    print("motorinit successfully")

def motordeinit():
    GPIO.cleanup()
    print("motordeinit successfully")    

#as for four phase stepping motor, four steps is a cycle. the function is used to drive the stepping motor clockwise or anticlockwise to take four steps    
def moveOnePeriod(direction,ms):    
    for j in range(0,4,1):      #cycle for power supply order
        for i in range(0,4,1):  #assign to each pin, a total of 4 pins
            if (direction == 1):#power supply order clockwise
                GPIO.output(motorPins[i],((CCWStep[j] == 1<<i) and GPIO.HIGH or GPIO.LOW))
            else :              #power supply order anticlockwise
                GPIO.output(motorPins[i],((CWStep[j] == 1<<i) and GPIO.HIGH or GPIO.LOW))
        if(ms<3):       #the delay can not be less than 3ms, otherwise it will exceed speed limit of the motor
            ms = 3
        time.sleep(ms*0.001)

def motorStop():
    for i in range(0,4,1):
        GPIO.output(motorPins[i],GPIO.LOW)

            
def moveSteps(direction, ms, steps):
     for i in range(steps):
         moveOnePeriod(direction, ms)

if __name__ == "__main__":
    motorinit()
    try:
       while(True):
        data=ser.read()
        if data[0] == 97:
            print(data[0])
            moveSteps(1,3,512)
        if data[0] == 98:
            print(data[0])
            moveSteps(0,3,512)
    except KeyboardInterrupt:
        motordeinit()

