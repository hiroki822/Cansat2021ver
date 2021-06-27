import sys
sys.path.append('/home/pi/desktop/Cansat2021ver/Calibration')
sys.path.append('/home/pi/desktop/Cansat2021ver/SensorModule/6-axis')
import math
import BMC050
import time


def angle(magx, magy, magx_off=0, magy_off=0):
    θ = math.degrees(math.atan((magy - magy_off) / (magx - magx_off)))

    if magx - magx_off > 0 and magy - magy_off > 0:  # First quadrant
        pass  # 0 <= θ <= 90
    elif magx - magx_off < 0 and magy - magy_off > 0:  # Second quadrant
        θ = 180 + θ  # 90 <= θ <= 180
    elif magx - magx_off < 0 and magy - magy_off < 0:  # Third quadrant
        θ = θ + 180  # 180 <= θ <= 270
    elif magx - magx_off > 0 and magy - magy_off < 0:  # Fourth quadrant
        θ = 360 + θ  # 270 <= θ <= 360

    return θ


if __name__ == '__main__':
    BMC050.bmc050_setup()
    magdata = BMC050.mag_dataRead()
    mag_x = magdata[0]
    mag_y = magdata[1]
    while True:
        magdata = BMC050.mag_dataRead()
        mag_x = magdata[0]
        mag_y = magdata[1]
        θ = angle(mag_x, mag_y)
        print(θ)
        time.sleep(0.5)
