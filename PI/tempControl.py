#!/usr/bin/python

import io
import sys
import fcntl
import copy
import string
import warnings

from LED_PWM import *

def shutDownLEDs(ledPWM, ledStatus):
	ledStop(ledPWM)
	return False #return value sets ledStatus

def startUpLEDs(ledPWM, ledStatus):
	ledStart(ledPWM)
	return True

def tempControl(tempValue, ledPWM, ledStatus):
	tempMax = 102
	tempLow = 87
	tempHigh = 97

	if(tempValue > tempMax):
		maxWarning = ("Temperature is currently", tempValue, " and has exceeded maximum of", tempMax, "degrees")
		warnings.warn(maxWarning)
		ledStatus = shutDownLEDs(ledPWM, ledStatus)

	elif(tempValue > tempHigh):
		print ("Temperature is currently", tempValue, "and greater than the higher range of", tempHigh, "degrees")
		if(ledStatus):
			ledStatus = shutDownLEDs(ledPWM, ledStatus)
			print("Shutting down heater (LED)")
		else:
			print("Heater (LED) is already off")

	elif(tempValue < tempLow):
		print ("Temperature is currently", tempValue, "and is less than the lower range of", tempLow, "degrees")
		if(not ledStatus):
			ledStatus = startUpLEDs(ledPWM, ledStatus)
			print("Turning on heater (LED)")
		else:
			print("Heater (LED) is already on")

	else:
		print ("Temperature is currently", tempValue, "and is within the range of", tempLow, "degrees to", tempHigh, "degrees")
	return ledStatus

