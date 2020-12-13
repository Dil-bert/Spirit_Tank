#!/usr/bin/python


import RPi.GPIO as GPIO

def ledInit():
	LED_GPIO = 12	#Sets LED to GPIO 12
	onTime=10e-6 	#10 microseconds
	offTime=10e-3 	#10 milliseconds
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(LED_GPIO, GPIO.OUT)
	frequency = 1/(onTime + offTime)
	LED_PWM = GPIO.PWM(LED_GPIO, frequency)
	duty_cycle = 10e-6/(onTime + offTime)
	return LED_PWM

def ledStart(LED_PWM):
	onTime=10e-6 	#10 microseconds
	offTime=10e-3 	#10 milliseconds
	duty_cycle = onTime/(onTime + offTime)
	LED_PWM.start(duty_cycle)
	
def ledStop(LED_PWM):
	LED_PWM.stop()
	#GPIO.cleanup() Commented out as it left the led on
