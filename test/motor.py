from gpiozero import Motor
from time import sleep

Rpin1 = 17
Rpin2 = 18

Lpin1 = 19
Lpin2 = 20


motor = Motor(Rpin1, Rpin2)
motor.forward(0.2)
sleep(2)
motor.backward(0.5)
sleep(3)
motor.stop()


motor = Motor(Lpin1, Lpin2)
motor.forward(0.2)
sleep(2)
motor.backward(0.5)
sleep(3)
motor.stop()