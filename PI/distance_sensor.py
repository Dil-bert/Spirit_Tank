#!/usr/bin/python

 #  Hardware Connections:
 #  Raspberry Pi | HC-SR04
 #   -------------------
 #     5V        |   VCC
 #     GPIO 23   |   Trig
 #     GPIO 24   |   Echo
 #     GND       |   GND


import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library
def read_distance():
  GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering 
  GPIO.setwarnings(False)


  TRIG = 23                                  #Associate pin 23 to TRIG
  ECHO = 24                                  #Associate pin 24 to ECHO

  #print "Distance measurement in progress"

  GPIO.setup(TRIG,GPIO.OUT)                  #Set pin as GPIO out
  GPIO.setup(ECHO,GPIO.IN)                   #Set pin as GPIO in


  GPIO.output(TRIG, False)                 #Set TRIG as LOW
  #print "Waitng For Sensor To Settle"
  time.sleep(2)                            #Delay of 2 seconds

  GPIO.output(TRIG, True)                  #Set TRIG as HIGH
  time.sleep(0.00001)                      #Delay of 0.00001 seconds
  GPIO.output(TRIG, False)                 #Set TRIG as LOW

  while GPIO.input(ECHO)==0:               #Check whether the ECHO is LOW
    pulse_start = time.time()              #Saves the last known time of LOW pulse

  while GPIO.input(ECHO)==1:               #Check whether the ECHO is HIGH
    pulse_end = time.time()                #Saves the last known time of HIGH pulse 

  pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

  velocity = 34300                         #Speed of sound, 343 meters/second -> 34300 centimeters/second

  distance = pulse_duration * velocity / 2 #Multiply pulse duration by velocity divided by 2 to get distance
  distance = round(distance, 2)            #Round to two decimal points
  


  if distance > 2 and distance < 400:      #Check whether the distance is within range
    return distance - 0.5                  #Return distance with 0.5cm calibration
  else:
    print ("Water Out Of Range")                   #display out of range
    return -1
