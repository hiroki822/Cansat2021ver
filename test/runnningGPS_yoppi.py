from threading import Thread
import traceback
import time
import pigpio
import Calibration
import Stuck
import motor
import stuck
import GPS
import BMC050
import Xbee
import gps_navigate
import numpy as np
import sys
# このパス後で調整必要　by oosim
sys.path.append('/home/pi/git/kimuralab/SensorModule/Communication')
sys.path.append('/home/pi/git/kimuralab/SensorModule/Camera')
sys.path.append('/home/pi/git/kimuralab/SensorModule/GPS')
sys.path.append('/home/pi/git/kimuralab/SensorModule/Motor')
sys.path.append('/home/pi/git/kimuralab//Calibration')
sys.path.append('/home/pi/git/kimuralab/IntegratedProgram/Stuck')

# --- original module ---#

# --- must be installed module ---#
# import numpy as np

# --- default module ---#
# import difflib

GPS_data = [0.0, 0.0, 0.0, 0.0, 0.0]


def timer(t):
    global cond
    time.sleep(t)
    cond = False


if __name__ == "__main__":
    BMC050.BMC050_setup()
    GPS.openGPS()
    print('Run Phase Start!')
    # --- difine goal latitude and longitude ---#
    lon2 = 139.90833592590076
    lat2 = 35.91817558805946

    # ------------- program start -------------#
    direction = Calibration.calculate_direction(lon2, lat2)
    goal_distance = direction['distance']
    print('goal distance = ' + str(goal_distance))
    # ------------- GPS navigate -------------#
    while goal_distance >= 15:  # この値調整必要
        # ------------- Calibration -------------#
        print('Calibration Start')
        # --- calculate offset ---#
        magdata = Calibration.magdata_matrix()
        magdata_offset = Calibration.calculate_offset(magdata)
        magx_off = magdata_offset[3]
        magy_off = magdata_offset[4]
        magz_off = magdata_offset[5]
        time.sleep(1)
        # --- calculate θ ---#
        data = Calibration.get_data()
        magx = data[0]
        magy = data[1]
        # --- 0 <= θ <= 360 ---#
        θ = Calibration.calculate_angle_2D(magx, magy, magx_off, magy_off)
        # ------------- rotate contorol -------------#
        Calibration.rotate_control(θ, lon2, lat2)
        location = Stuck.stuck_detection1()
        longitude_past = location[0]
        latitude_past = location[1]
        # --- initialize count ---#
        loop_count = 0
        stuck_count = 0

        # --- calculate  goal direction ---#
        direction = Calibration.calculate_direction(lon2, lat2)
        goal_distance = direction["distance"]
        print('goal distance =' + str(goal_distance))
        if goal_distance <= 15:
            break

        data = Calibration.get_data()
        magx = data[0]
        magy = data[1]
       # --- 0 <= θ <= 360 ---#
        theta = Calibration.calculate_angle_2D(
            magx, magy, magx_off, magy_off)
        azimuth = direction["azimuth1"]
        theta = theta-azimuth

        # ローバーを目標地点に合わせる
        # パラメータ要確認
        Xbee.str_trans('theta = '+str(theta)+'---回転調整開始！')
        count = 0
        while abs(theta) > 30:
            Xbee.str_trans(str(count))
            if count > 6:
                Xbee.str_trans('スタックもしくはこの場所が適切ではない')
                stuck.stuck_avoid()

            if abs(theta) <= 180:
                if abs(theta) <= 60:
                    Xbee.str_trans('theta = '+str(theta)+'---回転開始ver1')
                    motor.motor_move(
                        np.sign(theta)*0.5, -1*np.sign(theta)*0.5, 3)
                    motor.stop()

                elif abs(theta) <= 180:
                    Xbee.str_trans('theta = '+str(theta)+'---回転開始ver2')
                    motor.motor_move(-np.sign(theta)
                                     * 0.5, np.sign(theta)*0.5, 3)
                    motor.motor_stop()
            elif abs(theta) > 180:
                if abs(theta) >= 300:
                    Xbee.str_trans('theta = '+str(theta)+'---回転開始ver3')
                    motor.motor_move(-np.sign(theta)
                                     * 0.5, np.sign(theta)*0.5, 5)
                    motor.motor_stop()
                elif abs(theta) > 180:
                    Xbee.str_trans('theta = '+str(theta)+'---回転開始ver4')
                    motor.motor_move(
                        np.sign(theta)*0.5, -np.sign(theta)*0.5, 5)
                    motor.motor_stop()
            count += 1

        Xbee.str_trans('theta = '+str(theta)+'---回転終了!!!')

        # パラメータ要確認
        Xbee.str_trans('theta = '+str(theta)+'---直進開始')
        motor.motor_move(0.8, 0.8, 0.2)
        if stuck.stuck_duj():
            stuck.stuck_avoid()
        motor.motor_move(0.8, 0.8, 10)

     # --- calculate  goal direction ---#
        direction = Calibration.calculate_direction(lon2, lat2)
        goal_distance = direction["distance"]
