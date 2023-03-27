from stepmotor import motor
import time

def test_position():
    motor1=motor(12, 16, 18, 22)
    assert motor1.position==0
    motor1.motorinit()
    motor1.move(2048,'cw')
    time.sleep(10)
    assert motor1.position==360