import RPi.GPIO as GPIO
import time
import threading

class motor():
     
    def __init__(self,phaseA,phaseB,phaseC,phaseD):
        self.stop=False
        self.phaseA=phaseA
        self.phaseB=phaseB
        self.phaseC=phaseC
        self.phaseD=phaseD
        self.phase_state=8  #ABCD = 1000
        #self.position=0
        self.steps=0
    def motorinit(self):
        if GPIO.getmode() == None:
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
        elif direction == 'ccw':
            if self.phase_state==8:
                self.phase_state=1
            else:
                self.phase_state=self.phase_state << 1
        if self.phase_state==1 and self.stop==False:
            GPIO.output(self.phaseA,GPIO.LOW)
            GPIO.output(self.phaseB,GPIO.LOW)
            GPIO.output(self.phaseC,GPIO.LOW)
            GPIO.output(self.phaseD,GPIO.HIGH)
        if self.phase_state==2 and self.stop==False:
            GPIO.output(self.phaseA,GPIO.LOW)
            GPIO.output(self.phaseB,GPIO.LOW)
            GPIO.output(self.phaseC,GPIO.HIGH)
            GPIO.output(self.phaseD,GPIO.LOW)
        if self.phase_state==4 and self.stop==False:
            GPIO.output(self.phaseA,GPIO.LOW)
            GPIO.output(self.phaseB,GPIO.HIGH)
            GPIO.output(self.phaseC,GPIO.LOW)
            GPIO.output(self.phaseD,GPIO.LOW)
        if self.phase_state==8 and self.stop==False:
            GPIO.output(self.phaseA,GPIO.HIGH)
            GPIO.output(self.phaseB,GPIO.LOW)
            GPIO.output(self.phaseC,GPIO.LOW)
            GPIO.output(self.phaseD,GPIO.LOW)

    def move(self,steps,direction):
        move_theard=threading.Thread(target=self.motorMove,args=(steps,direction,))
        move_theard.start()
        
    def motorMove(self,steps,direction):        
         for i in range(steps):
            if self.stop==True:
                break
            if direction=='cw':
                #self.position+=360/2048
                self.steps+=1
            else:
                #self.position-=360/2048
                self.steps-=1
            self.onestep(direction)
            time.sleep(0.005) 
         self.motorStop()
         print(self.steps)
   
    def motorStop(self):
        GPIO.output(self.phaseA,GPIO.LOW)
        GPIO.output(self.phaseB,GPIO.LOW)
        GPIO.output(self.phaseC,GPIO.LOW)
        GPIO.output(self.phaseD,GPIO.LOW)
        self.stop=True