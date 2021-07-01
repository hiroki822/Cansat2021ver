from gpiozero import Motor
from time import sleep
import sys
sys.path.append('/home/pi/desktop/Cansat2021ver/SensorModule/6-axis')
sys.path.append('/home/pi/desktop/Cansat2021ver/SensorModule/Communication')
sys.path.append('/home/pi/desktop/Cansat2021ver/SensorModule/Motor')
# ピン番号は仮
Rpin1 = 17
Rpin2 = 18

Lpin1 = 19
Lpin2 = 20


def run_s(strength, time=10):
    Rpin1 = 17
    Rpin2 = 18
    Lpin1 = 19
    Lpin2 = 20
    motor = Motor(Rpin1, Rpin2)
    t = 0
    while t < 10:
        t_start = time.time()
        if Motor.stuck_jud(strength):
            # stuck avoid 関数ここにぶち込む
            break
        else:
            motor = Motor(Rpin1, Rpin2)
            motor.forward(strength)
            sleep(time)
        t_end = time.time()
        t = t_end-t_start
