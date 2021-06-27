import sys
sys.path.append('/home/pi/desktop/Cansat2021ver/Calibration')
sys.path.append('/home/pi/desktop/Cansat2021ver/SensorModule/6-axis')
import math
import BMC050


def calculate_angle_2D(magx, magy, magx_off, magy_off):
    # --- recognize rover's direction ---#
    # --- North = 0 , θ = (direction of sensor) ---#
    # --- -90 <= θ <= 90 ---#
    global θ
    θ = math.degrees(math.atan((magy - magy_off) / (magx - magx_off)))
    if θ >= 0:
        if magx - magx_off < 0 and magy - magy_off < 0:  # Third quadrant
            θ = θ + 180  # 180 <= θ <= 270
        if magx - magx_off > 0 and magy - magy_off > 0:  # First quadrant
            pass  # 0 <= θ <= 90
    else:
        if magx - magx_off < 0 and magy - magy_off > 0:  # Second quadrant
            θ = 180 + θ  # 90 <= θ <= 180
        if magx - magx_off > 0 and magy - magy_off < 0:  # Fourth quadrant
            θ = 360 + θ  # 270 <= θ <= 360

    # --- Half turn  ---#
    θ += 180
    if θ >= 360:
        θ -= 360
    # print('magx-magx_off = '+str(magx-magx_off))
    # print('magy-magy_off = '+str(magy-magy_off))
    print('calculate:θ = ' + str(θ))
    # --- 0 <= θ <= 360 ---#
    return θ


if __name__ == '__main__':
    BMC050.bmc050_setup()
    while True:
        magdata = BMC050.mag_dataRead()
        mag_x = magdata[0]
        mag_y = magdata[1]
        θ = calculate_angle_2D(mag_x, mag_y, 0, 0)
        print(θ)
