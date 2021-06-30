from time import sleep
from gpiozero import Motor
import BMC050
import sys
sys.path.append('/home/pi/desktop/Cansat2021ver/SensorModule/6-axis')
sys.path.append('/home/pi/desktop/Cansat2021ver/SensorModule/Motor')
sys.path.append('/home/pi/desktop/Cansat2021ver/SensorModule/Communication/a')


def stuck(thd=1):
    BMC050.bmc050_setup()
    motor = Motor(Rpin1, Rpin2)
    while 1:
        motor.forward(0.2)
        sleep(0.3)
        accdata = BMC050.acc_data()
        acc_x = accdata[0]
        acc_y = accdata[1]
        acc_z = accdata[2]
        acc = (acc_x**2 + acc_y**2 + acc_z**2)**0.5
        if acc < thd:
            print('スタックした　：acc = '+str(acc))
            send.str_trans('スタックした　：acc = '+str(acc))
            motor.stop()
            break
        else:
            print('まだしてない　:acc = '+str(acc))
            send.str_trans('まだしてない　:acc = '+str(acc))
            motor.forward(0.2)
            sleep(2)


if __name__ == '__main__':
    Rpin1 = 17
    Rpin2 = 18

    Lpin1 = 19
    Lpin2 = 20
    stuck(12)
