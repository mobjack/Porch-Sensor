#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep 
import logging
import random
import time
import sys

logfile = '/home/pi/scripts/porch-sensor/motion.log'

class Motion:

    def __init__(self):
        self.motion_pin = 11
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.motion_pin, GPIO.IN)

    def status(self):
        if GPIO.input(self.motion_pin) == 1:
            return(True)
        else:
            return(False)

class Distance:

    def __init__(self):

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        #set GPIO Pins
        self.trigger = 38
        self.echo = 36
 
        #set GPIO direction (IN / OUT)
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

        GPIO.output(self.trigger, True)
        # set Trigger after 0.01ms to LOW
        sleep(0.00001)
        GPIO.output(self.trigger, False)

    def alert(self):
        #print('dist called')
        start_time = float()
        stop_time = float()

        GPIO.output(self.trigger, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.trigger, GPIO.LOW)

        # save start_time
        while GPIO.input(self.echo) == 0:
            start_time = time.time()
 
        # save time of arrival
        while GPIO.input(self.echo) == 1:
            stop_time = time.time()
 

        time_calc = stop_time - start_time
        distance = (time_calc * 34300) / 2

        #print(distance)
        return(distance)

class Light:
    
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.led_gr = 16
        self.led_red = 15
        #Light setup
        GPIO.setup(self.led_gr, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.led_red, GPIO.OUT, initial=GPIO.LOW)
        GPIO.output(self.led_red, GPIO.LOW)
        GPIO.output(self.led_gr, GPIO.HIGH)
  
    def alert(self, alert_status): # False = Off ; True = On
        if alert_status == True:
            GPIO.output(self.led_red, GPIO.HIGH) 
            GPIO.output(self.led_gr, GPIO.LOW)
        else:
            GPIO.output(self.led_gr, GPIO.HIGH) 
            GPIO.output(self.led_red, GPIO.LOW)
            
    def alloff(self):
        GPIO.output(self.led_red, GPIO.LOW)
        GPIO.output(self.led_gr, GPIO.LOW) 

def logit(funct, logmsg):
    debug = True
    if debug == False:
        return(None)
    else:
        message = funct.upper() + ' : ' + logmsg
        logformat = "%(asctime)s %(message)s"
        logging.basicConfig(filename = logfile, level = logging.DEBUG, format = logformat)
        logger = logging.getLogger()
        logger.debug(message)

def main():
    
    logit('main', 'Script Started')
    motion_ctl = Motion()
    dist_ctl = Distance()
    light_ctl = Light()
    
    try:
        while True: # Run forever

            stable_dist = float(120)
            if motion_ctl.status() == True:
                distance_check = dist_ctl.alert()
                if distance_check < stable_dist:
                    logit('motion', 'Activity detected distance is %s' % str(distance_check))
                    #print('Alert Here! ' + str(distance_check))
                    light_ctl.alert(True)
                    sleep(10)
            else:
                light_ctl.alert(False)
            light_ctl.alert(False)
            sleep(.05)

    except KeyboardInterrupt:
        logit('main', 'Script stopped manually')
        light_ctl.alloff()
        GPIO.cleanup()

    logit('main', 'Script exit')


if __name__ == '__main__':
    main()

