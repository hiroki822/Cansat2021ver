import sys
sys.path.append('/home/pi/Desktop/Cansat2021ver/Other')
sys.path.append('/home/pi/Desktop/Cansat2021ver/SensorModule/Camera')
sys.path.append('/home/pi/Desktop/Cansat2021ver/SensorModule/Emvironmental')
sys.path.append('/home/pi/Desktop/Cansat2021ver/SensorModule/Communication')
import panorama
import Capture
import BMC050
import Xbee


def shooting(magx_off, magy_off, path):
    """
    パノラマ撮影用の関数
    引数は磁気のオフセット
    """
    magdata = BMC050.mag_dataRead()
    magx = magdata[0]
    magy = magdata[1]
    preθ = Calibration.calculate_angle_2D(magx, magy, magx_off, magy_off)
    sumθ = 0
    deltaθ = 0
    Xbee.str_trans('whileスタート preθ:{0}'.format(preθ))

    while sumθ <= 360:
        Captrue.Capture(path)
        motorTest.motor_move(-1, 1, 1) #調整するところ？
        magdata = BMC050.mag_dataRead()
        magx = magdata[0]
        magy = magdata[1]
        latestθ = Calibration.calculate_angle_2D(magx, magy, magx_off, magy_off)
        if preθ >= 300 and latestθ <= 100:
            latestθ += 360
        deltaθ = preθ - latestθ
        sumθ += deltaθ
        if latestθ >= 360:
            latestθ -= 360
        preθ = latestθ
        Xbee.str_trans('sumθ:', sumθ, ' preθ:', preθ, ' deltaθ:', deltaθ)