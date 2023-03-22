#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from rupcom import Serial_com
from stepmotor import motor

if __name__ == "__main__":
    ser=Serial_com()
    ser.open("/dev/ttyAMA0",9600)
    zmotor=motor(12, 16, 18, 22)
    zmotor.motorinit()
    try:
       while True:
           message=ser.read()
           print(message)
           zmotor.move(2048,'cw')
           time.sleep(2)
           
    except KeyboardInterrupt:
        zmotor.motordeinit()
        ser.close()

