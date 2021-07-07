from gpiozero import Motor
from time import sleep
import time
import BMC050
import stuck
import Xbee
import sys
sys.path.append('/home/pi/desktop/Cansat2021ver/SensorModule/6-axis')
sys.path.append('/home/pi/desktop/Cansat2021ver/SensorModule/Motor')
sys.path.append('/home/pi/desktop/Cansat2021ver/SensorModule/Communication')

# ピン番号は仮
Rpin1 = 17
Rpin2 = 18

Lpin1 = 19
Lpin2 = 20


def motor_stop(x=1):
    Rpin1 = 19
    Rpin2 = 26
    Lpin1 = 5
    Lpin2 = 6
    motor_r = Motor(Rpin1, Rpin2)
    motor_l = Motor(Lpin1, Lpin2)
    motor_r.stop()
    motor_l.stop()
    time.sleep(x)


def motor_move(strength_l, strength_r, time):
    Rpin1 = 19
    Rpin2 = 26
    Lpin1 = 5
    Lpin2 = 6
    # 前進するときのみスタック判定
    if strength_r >= 0 & strength_l >= 0:
        motor_r = Motor(Rpin1, Rpin2)
        motor_l = Motor(Lpin1, Lpin2)
        motor_r.forward(strength_r)
        motor_l.forward(strength_l)
        sleep(time)
    # 後進
    elif strength_r < 0 & strength_l < 0:
        motor_r = Motor(Rpin1, Rpin2)
        motor_l = Motor(Lpin1, Lpin2)
        motor_r.backward(abs(strength_r))
        motor_l.backward(abs(strength_l))
        sleep(time)
    # 右回転
    elif strength_r >= 0 & strength_l < 0:
        motor_r = Motor(Rpin1, Rpin2)
        motor_l = Motor(Lpin1, Lpin2)
        motor_r.forkward(abs(strength_r))
        motor_l.backward(abs(strength_l))
        sleep(time)
    # 左回転
    elif strength_r < 0 & strength_l >= 0:
        motor_r = Motor(Rpin1, Rpin2)
        motor_l = Motor(Lpin1, Lpin2)
        motor_r.backward(abs(strength_r))
        motor_l.forkward(abs(strength_l))
        sleep(time)


# スタックavoid関数用です
def motor_move_avoid(strength_l, strength_r, time):
    Rpin1 = 19
    Rpin2 = 26
    Lpin1 = 5
    Lpin2 = 6
    # 前進するときのみスタック判定
    if strength_r >= 0 & strength_l >= 0:
        motor_r = Motor(Rpin1, Rpin2)
        motor_l = Motor(Lpin1, Lpin2)
        motor_r.forward(strength_r)
        motor_l.forward(strength_l)
        sleep(time)
        motor_r.stop()
        motor_l.stop()

    # 後進
    elif strength_r < 0 & strength_l < 0:
        motor_r = Motor(Rpin1, Rpin2)
        motor_l = Motor(Lpin1, Lpin2)
        motor_r.backward(abs(strength_r))
        motor_l.backward(abs(strength_l))
        sleep(time)
        motor_r.stop()
        motor_l.stop()
    # 右回転
    elif strength_r >= 0 & strength_l < 0:
        motor_r = Motor(Rpin1, Rpin2)
        motor_l = Motor(Lpin1, Lpin2)
        motor_r.forkward(abs(strength_r))
        motor_l.backward(abs(strength_l))
        sleep(time)
        motor_r.stop()
        motor_l.stop()
    # 左回転
    elif strength_r < 0 & strength_l >= 0:
        motor_r = Motor(Rpin1, Rpin2)
        motor_l = Motor(Lpin1, Lpin2)
        motor_r.backward(abs(strength_r))
        motor_l.forkward(abs(strength_l))
        sleep(time)
        motor_r.stop()
        motor_l.stop()


# ------------
 bool_stuck = stuck.stuck_jud()
        if bool_stuck:
            Xbee.str_trans('スタックしました一回目')
            motor_r.stop()
            motor_l.stop()
            # 一応もう一回スタック判定確かめる
            motor_r.forward(strength_r)
            motor_l.forward(strength_l)
            sleep(0.2)
            bool_stuck = stuck.stuck_jud()
            if bool_stuck:
                Xbee.str_trans('スタックしました二回目')
                motor_r.stop()
                motor_l.stop()
                # スタック回避関数ぶち込む
            else:
                pass
        else:
            Xbee.str_trans('直進中')
            sleep(time-0.2)
            motor_r.stop()
            motor_l.stop()
# ------------




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
