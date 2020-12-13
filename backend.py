#!/usr/bin/python

import io
import sys
import fcntl
import time
import copy
import string
import re
import pickle

from datetime import datetime
from Spirit_main import*
from tempControl import*
from phControl import*
from LED_PWM import*

#see if easier way to import from file
from i2c import *

import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library

from distance_sensor import (
    read_distance
)

class Spirit_main(QtWidgets.QMainWindow):
	def __init__(self):
		super(Spirit_main, self).__init__()
		
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		
		

def fill_tank(device_list, full_distance):
	fill_distance = read_distance()
	while (fill_distance > full_distance):
		### PUMPING
		send_pumpValue(1,device_list)
		time.sleep(1.5)
		fill_distance = read_distance()
	### FULL
	return

def deviceStr2Float(deviceString): #converts device response strings to float values
	#	Parses the device response, produces a list with the string for the decimal value reading, 
    #Converts the string to a floating point value and prints it out.
    deviceReading = re.findall(r"[-+]?\d*\.\d+", deviceString)
    deviceReading = str(''.join(deviceReading))
    deviceValue = float(deviceReading)
    return deviceValue 

def send_pumpValue(volume, device_list):
	addr = 103
	available = False
	
	distance = read_distance()
	print ("Distance from sensor is:", distance,"cm")
	for i in device_list:
		if(i.address == int(addr)):
			device = i
			available = True
	if(available):
		deviceReturn = device.query("D,9")
		return
		
	else:
		print("Sensor is not available")
		return

def getDeviceValue(addr, device_list): #returns float device value
	# go through the devices to figure out if its available
	# and send command to it if it is
	available = False
	for i in device_list:
		if(i.address == int(addr)):
			device = i
			available = True
	if(available):
		deviceReturn = device.query("R")
		return deviceStr2Float(deviceReturn)
		
	else:
		print('Sensor is not available')
		return -1

def unsafe_state(safe_bool):
	try:
		unsafe_state_log = open('UnsafeState.dat', 'wb')
		pickle.dump(datetime.now(),unsafe_state_log)
		unsafe_state_log.close()
	except IOError:
		print('Error writing to UnsafeState.dat')
	finally:
		safe_bool = False
		return safe_bool
		

def getSafetyState(safe_bool):
	delta = timedelta(
	days=1,
	seconds=0,
	microseconds=0,
	milliseconds=0,
	minutes=0,
	hours=0,
	weeks=0)
	try:
		unsafe_state_log = open("UnsafeState.dat", "rb")
		last_unsafe_time = pickle.load(unsafe_state_log)
		unsafe_state_log.close()
		temp = datetime.now() - last_unsafe_time
		if temp > delta:
			safe_bool = True
		else:
			safe_bool = False
		
	except IOError:
		print('Critical Error reading UnsafeState.dat \n')
		print('UnsafeState.dat will be created and set to unsafe \n')
		print('Bug report requested \n')
		safe_bool = unsafe_state(safe_bool)
	finally:
		return safe_bool

def main():
	
	
	app = QtWidgets.QApplication(sys.argv)
	##Spirit_main()
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	#sys.exit(app.exec_())
	
	PH_ADDR = "99"
	TEMP_ADDR = "102"
	PUMP_ADDR = "103"
	
	### TANK DEPENDANT THINK OF WAY TO AVOID TANK DEPENDANCE
	##MIN_HEIGHT_FIRST =
	##MIN_HEIGHT_SECOND =
	##MIN_HEIGHT_FULL =
	
	PH_DANGER = 9.5
	PH_TRIGGER = 10
	PH_CO2_MIN = 10.3
	
	TEMP_MIN = 93
	TEMP_MAX = 101
	TEMP_IDEAL = 97
	
	STATES = ('empty', 'first', 'second', 'final')
	
	state = STATES[0]
	safe_bool = False
	harvestable = False
	run = True
    
	##ledPWM = ledInit()
    
	device_list = get_devices()
	device = device_list[0]
	real_raw_input = vars(__builtins__).get('raw_input', input)
   
    ###	TODO USING QT
    ### Check for saved state of culture,
    ###  Verify State of culture.
    ###	 Ask for state of culture at initial boot.
    
	try:
		saved_state_file = open("SaveState.txt")
		state = saved_state_file.read()
		saved_state_file.close()
	except IOError:
		saved_state_file = open("SaveState.txt", "w")
		state = STATES[0]
		saved_state_file.write(state)
		saved_state_file.close()
	finally:
		safe_bool = unsafe_state(safe_bool)
		##Output culture state Verify and correct via user input
	
		
	while True:
		ph_value = getDeviceValue(PH_ADDR, device_list)
		ui.ph_text_out.insertPlainText("99")
		temp_value = getDeviceValue(TEMP_ADDR, device_list)
		
		if ph_value <= PH_DANGER:
			safe_bool = unsafe_state(safe_bool)
			##  dispense ph_up solution.
		if ph_value > PH_DANGER:
			getSafetyState(safe_bool)
		if((state == STATES[3])&(safe_bool)):
			harvestable = True
		else:
			harvestable = False
		## Seperate thread control temp
		## Seperate thread control Dispensing
		### TODO Display culture status and other event messages
	

	
		

                    
if __name__ == '__main__':
    main()
