import sys
sys.path.append('/home/pi/Desktop/Cansat2021ver/SensorModule/6-axis')
sys.path.append('/home/pi/Desktop/Cansat2021ver/SensorModule/Communication')
sys.path.append('/home/pi/Desktop/Cansat2021ver/Calibration')


import motorTest
import BMC050
import Calibration
import Xbee

def rotation(magx_off, magy_off,count=1):
    """
    回転テスト用(パノラマ撮影もこれからスタート？)
    引数は磁気のオフセット、countは回転する回数
    プラスマイナスを行き来する場合は使えないから改善する必要あり2021/07/04
    takayama
    """
    for _ in range(count):
        magdata = BMC050.mag_dataRead()
        magx = magdata[0]
        magy = magdata[1]
        preθ = Calibration.calculate_angle_2D(magx, magy, 0, 0)
        Xbee
        sumθ = 0
        deltaθ = 0
        Xbee.str_trans(preθ + ' whileスタート')

        while sumθ <= 360:
            motorTest.motor_move(1, -1, 1)
            magdata = BMC050.mag_dataRead()
            magx = magdata[0]
            magy = magdata[1]
            latestθ = Calibration.calculate_angle_2D(magx, magy, 0, 0)
            deltaθ = preθ - latestθ
            sumθ += deltaθ
            preθ = latestθ
            Xbee.str_trans('sumθ:', sumθ, ' preθ:', preθ, ' deltaθ:', deltaθ)


if __name__ == "__main__":
    try:
        BMC050.bmc050_setup()
        magdata = Calibration.magdata_matrix()  #magdata_matrix()内を変更する必要あり2021/07/04
        _, _, _, magx_off, magy_off, _ = Calibration.calculate_offset(magdata)
        rotation(magx_off, magy_off)
    except:
        print('error')