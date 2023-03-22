import serial

class Serial_com():
    def __init__(self):
        self.serialCommunication=None
    
    def read(self):
        message=None
        if self.serialCommunication.inWaiting()>0:
            message=self.serialCommunication.read_until()
        return message
    
    def write(self,message: str):
        self.serialCommunication.write(message.encode())

    def open(self,com_port,baudrate):
        self.serialCommunication=serial.Serial(com_port,baudrate)
        print("serial Communication established")
    
    def close(self):
        self.serialCommunication.reset_input_buffer()
        self.serialCommunication.close()
        print("serial Communication closed")
