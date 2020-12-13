#!/usr/bin/python

import io
import sys
import fcntl
import copy
import string
import warnings

from LED_PWM import *

def shutDownLEDs(ledPWM):
	ledStop(ledPWM)
	return False #return value sets ledStatus

def startUpLEDs(ledPWM):
	ledStart(ledPWM)
	return True

def phControl(phValue, ledPWM, ledStatus):
	phMax = 9
	phLow = 6
	phHigh = 8

	if(phValue > phMax):
		warnMessage = "pH is currently", phValue, " and has exceeded maximum of", phMax
		warnings.warn(warnMessage)
		ledStatus = shutDownLEDs(ledPWM)

	elif(phValue > phHigh):
		print ("ph is currently", phValue, "and greater than the higher range of", phHigh)
		if(ledStatus):
			ledStatus = shutDownLEDs(ledPWM)
			print("Turning off pH up solution dispenser (LED)")
		else:
			print("pH up solution dispenser (LED) is off")

	elif(phValue < phLow):
		print( "ph is currently", phValue, "and is less than the lower range of", phLow)
		if(not ledStatus):
			ledStatus = startUpLEDs(ledPWM)
			print("Dispensing pH up solution (LED)")
		else:
			print("pH solution (LED) is already being dispensed")

	else:
		print ("pH is currently", phValue, "and is within the range of", phLow, "to", phHigh)
	return ledStatus

