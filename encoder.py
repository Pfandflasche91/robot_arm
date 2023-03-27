import RPi.GPIO as GPIO
import time
import threading

class encoder():
    def __init__(self,pin) -> None:
        self.pin=pin
        self.timestamp=0
        self.blades_per_rotation=20
        self.v=0    
    def ecoderInit(self):
        if GPIO.getmode() == None:
            GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin,GPIO.IN)
        GPIO.add_event_detect(self.pin,GPIO.RISING,callback=self.speed_callback,bouncetime=50)
        print("encoderinit successfully")
    
    def getspeed(self):
        return self.v

    
    def speed_callback(self,test):
        self.v=(360/self.blades_per_rotation)/(time.time()-self.timestamp)
        self.timestamp=time.time()

