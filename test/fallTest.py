# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/IM920')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BME280')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Camera')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/TSL2561')
sys.path.append('/home/pi/git/kimuralab/Detection/ParachuteDetection')
sys.path.append('/home/pi/git/kimuralab/Detection/ReleaseAndLandingDetection')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Melting')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Motor')
sys.path.append('/home/pi/git/kimuralab/IntegratedProgram/ParaAvoidance')
sys.path.append('/home/pi/git/kimuralab/Other')
import time
import difflib
import pigpio
import serial
import binascii
# import IM920
import Xbee
import GPS
# import BMX055
import BMC050
import BME280
import Capture
import TSL2561
import Release
import Land
import GPS
import Melting
import Motor
import TSL2561
import ParaDetection
import ParaAvoidance
import Other

phaseChk = 0	#variable for phase Check
bme280str = ["temp", "pres", "hum", "alt"]												#variable to show bme280 returned variables
bmc050str = ["accx", "accy", "accz", "dirx", "diry", "dirz"]	#variable to show bmc050 returned variables
gpsstr = ["utctime", "lat", "lon", "sHeight", "gHeight"]								#variable to show GPS returned variables

gpsData = [0.0, 0.0, 0.0, 0.0, 0.0]
bme280Data = [0.0, 0.0, 0.0, 0.0]
bmx055data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

t_setup = 60	#variable to set waiting time after setup
t = 1			#Unknown Variable
x = 300			#time for release(loopx)
y = 180			#time for land(loopy)

t_start = 0.0	#time when program started


#variable used for releasejudge
releasepress = 0.3
pressreleasecount = 0
pressreleasejudge = 0

releasealt = 2
GArepeasecount = 0
gpsreleasejudge = 0

pi = pigpio.pi()

#variable used for landjudgment
presslandjudge = 0
gpslandjudge = 0
acclandjudge = 0
Landjudgment = [presslandjudge, gpslandjudge, acclandjudge]

#variable used for ParaDetection
LuxThd = 100
imgpath = "/home/pi/photo/photo"
width = 320
height = 240
H_min = 200
H_max = 10
S_thd = 120



paraExsist = 0 	#variable used for Para Detection

phaseLog = "/home/pi/log/phaseLog.txt"
waitingLog = "/home/pi/log/waitingLog.txt"
releaseLog = "/home/pi/log/releaseLog.txt"
landingLog = "/home/pi/log/landingLog.txt"
meltingLog = "/home/pi/log/meltingLog.txt"
paraAvoidanceLog = "/home/pi/log/paraAvoidanceLog.txt"


def setup():
	global phaseChk

	pi.set_mode(22,pigpio.OUTPUT)
	pi.write(22,1)	#IM920	Turn On
	pi.write(17,0)	#outcasing
	time.sleep(1)
	BME280.bme280_setup()
	BME280.bme280_calib_param()
	BMC050.bmc050_setup()
	GPS.openGPS()

	# with open(phaseLog, 'a') as f:
	# 	pass

	phaseChk = int(Other.phaseCheck(phaseLog))
	print(phaseChk)

def close():
	GPS.closeGPS()
	pi.write(22, 0)
	pi.write(17,0)
	Motor.motor(0, 0, 1)
	Motor.motor_stop()

if __name__ == "__main__":
	try:
		t_start = time.time()
		# ------------------- Setup Phase --------------------- #
		print("Program Start  {0}".format(time.time()))
		setup()
		print(phaseChk)
		# IM920.Send("Start")

		# ------------------- Waiting Phase --------------------- #
		Other.saveLog(phaseLog, "2", "Waiting Phase Started", time.time() - t_start)
		if phaseChk <= 2:
			t_wait_start = time.time()
			while(time.time() - t_wait_start <= t_setup):
				Other.saveLog(waitingLog, time.time() - t_start, GPS.readGPS(), BME280.bme280_read(), TSL2561.readLux(), BMC050.bmc050_read())
				print("Waiting")
				# IM920.Send("Sleep")
				time.sleep(1)
			# IM920.Send("Waiting Finished")
			pi.write(22, 0)		#IM920 Turn Off

		# ------------------- Release Phase ------------------- #
		Other.saveLog(phaseLog, "3", "Release Phase Started", time.time() - t_start)
		if phaseChk <= 3:
			tx1 = time.time()
			tx2 = tx1
			print("Releasing Judgement Program Start  {0}".format(time.time() - t_start))
			#loopx
			bme280Data = BME280.bme280_read()
			while tx2 - tx1 <= x:
				GAreleasecount, gpsreleasejudge = Release.gpsdetect(releasealt)
				pressreleasecount, pressreleasejudge = Release.pressdetect(releasepress)


				if gpsreleasejudge == 1 or pressreleasejudge == 1:
					break
				else:
					print("not yet")
				Other.saveLog(releaseLog, time.time() - t_start, GPS.readGPS(), BME280.bme280_read(), BMC050.bmc050_read())
				time.sleep(0.5)

				Other.saveLog(releaseLog, time.time() - t_start, GPS.readGPS(), BME280.bme280_read(), BMX055.bmx055_read())				
				time.sleep(0.5)

				tx2 = time.time()
			else:
				print("RELEASE TIMEOUT")
			print("THE ROVER HAS RELEASED")
			pi.write(22,1)
			time.sleep(2)
			# IM920.Send("RELEASE")

		# ------------------- Landing Phase ------------------- #
		Other.saveLog(phaseLog, "4", "Landing Phase Started", time.time() - t_start)
		if phaseChk <= 4:
			print("Landing Judgement Program Start  {0}".format(time.time() - t_start))
			ty1 = time.time()
			ty2 = ty1
			#loopy
			gpsData = GPS.readGPS()
			bme280Data = BME280.bme280_read()
			while ty2 - ty1 <= y:
				# IM920.Send("loopY")
				presslandjudge = 0
				gpslandjudge = 0
				acclandjudge = 0
				presslandjudge = Land.Pressdetect()
				gpslandjudge = Land.gpsdetect()
				acclanddetect = Land.accdetect()
				Landjudgment = [presslandjudge, gpslandjudge, acclandjudge]

				if Landjudgment.count(1) >= 2:
					print("THE ROVER HAS LANDED")
					break
				else:
					print("LAND NOT YET")
				gpsData = GPS.readGPS()
				bme280Data = BME280.bme280_read()
				bmc050data = BMC050.bmc050_read()
				Other.saveLog(landingLog, time.time() - t_start, GPS.readGPS(), BME280.bme280_read(), BMC050.bmc050_read())
				time.sleep(1)
				Other.saveLog(landingLog, time.time() - t_start, GPS.readGPS(), BME280.bme280_read(), BMC050.bmc050_read())
				time.sleep(1)
				Other.saveLog(landingLog, time.time() - t_start, GPS.readGPS(), BME280.bme280_read(), BMC050.bmc050_read())
				time.sleep(1)
				ty2 = time.time()
			else:
				print("LAND TIMEOUT")
			print("THE ROVER HAS LANDED")
			pi.write(22,1)
			# IM920.Send("LAND")

		# ------------------- Melting Phase ------------------- #
		# IM920.Send("Melt")
		Other.saveLog(phaseLog,"5", "Melting Phase Started", time.time() - t_start)
		if(phaseChk <= 5):
			print("Melting Phase Started")
			Other.saveLog(meltingLog, time.time() - t_start, GPS.readGPS(), "Melting Start")
			Melting.Melting()
			Other.saveLog(meltingLog, time.time() - t_start, GPS.readGPS(), "Melting Finished")

		# ------------------- ParaAvoidance Phase ------------------- #
		# IM920.Send("ParaAvo")
		Other.saveLog(phaseLog, "6", "ParaAvoidance Phase Started", time.time() - t_start)
		if(phaseChk <= 6):
			# IM920.Send('P7S')
			Other.saveLog(phaseLog, '7', 'Parachute Avoidance Phase Started', time.time() - t_start)
			t_ParaAvoidance_start = time.time()
			print('Parachute Avoidance Phase Started {}'.format(time.time() - t_start))

			while land_point_distance <= 1:
				try:
					flug = -1
					while flug == -1:
						# --- first parachute detection ---#
						flug, area, photoname = ParaDetection.ParaDetection("/home/pi/photo/photo", 320, 240, 200, 10, 120)
						Other.saveLog(ParaAvoidanceLog, 'ParaAvoidance', time.time() - t_start, flug, area, photoname, GPS.readGPS())
					ParaAvoidance.Parachute_Avoidance(flug, t_start)
					land_point_distance = ParaAvoidance.Parachute_area_judge(longitude_land, latitude_land)
					while land_point_distance == 0:
						land_point_distance = ParaAvoidance.Parachute_area_judge(longitude_land, latitude_land)
					print('land_point_distance = ', land_point_distance)

				except KeyboardInterrupt:
					print("Emergency!")
					run = pwm_control.Run()
					run.stop()

				except:
					run = pwm_control.Run()
					run.stop()
					print(traceback.format_exc())
			print('finish')
			# IM920.Send('P7F')
			phaseChk += 1
			print('phaseChk = ' + str(phaseChk))
			# print("ParaAvoidance Phase Started")
			# Other.saveLog(paraAvoidanceLog, time.time() - t_start, GPS.readGPS(), "ParaAvoidance Start")
			# print("START: Judge covered by Parachute")
			# ParaAvoidance.ParaJudge()
			# print("START: Parachute avoidance")
			# paraExsist = ParaAvoidance.ParaAvoidance()
			# Other.saveLog(paraAvoidanceLog, time.time() - t_start, GPS.readGPS(), paraExsist)
			# Other.saveLog(paraAvoidanceLog, time.time() - t_start, GPS.readGPS(), "ParaAvoidance Finished")

		# IM920.Send("Progam Finished")
		close()
	except KeyboardInterrupt:
		close()
		print("Keyboard Interrupt")
	except Exception as e:
		# IM920.Send("error")
		close()
		Other.saveLog("/home/pi/log/errorLog.txt", time.time() - t_start, "Error")
		print(e.message)
