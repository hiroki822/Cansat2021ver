from time import sleep
from gpiozero import Motor
import BMC050
import Xbee
import sys
sys.path.append('/home/pi/desktop/Cansat2021ver/SensorModule/6-axis')
sys.path.append('/home/pi/desktop/Cansat2021ver/SensorModule/Motor')
sys.path.append('/home/pi/desktop/Cansat2021ver/SensorModule/Communication')
sys.path.append('/home/pi/desktop/Cansat2021ver/SensorModule/Motor')


def stuck_jud(thd=1):
    Rpin1 = 19
    Rpin2 = 26
    Lpin1 = 5
    Lpin2 = 6
    motor_r = Motor(Rpin1, Rpin2)
    motor_l = Motor(Lpin1, Lpin2)
    BMC050.bmc050_setup()
    accdata = BMC050.acc_data()
    acc_x = accdata[0]
    acc_y = accdata[1]
    acc_z = accdata[2]
    acc = (acc_x**2 + acc_y**2 + acc_z**2)**0.5
    if acc < thd:
        print('スタックした')
        Xbee.str_trans('スタックした')
        motor_r.stop()
        motor_l.stop()
        return False
    else:
        print('まだしてない')
        Xbee.str_trans('まだしてない')
        return True


if __name__ == '__main__':
    Rpin1 = 17
    Rpin2 = 18

    Lpin1 = 19
    Lpin2 = 20
    stuck(12)
