#!/usr/bin/env python3

from twitter import TwitterChecker
from web import WebChecker
import time
import logging
import sys
import os
import atexit
from RPi import GPIO

# Set timezone
os.environ["TZ"] = "US/Eastern"

class CoffeeMachine():
    def __init__(self):
        # Configure Log
        LOGDIR = "/home/pi/Documents/coffeemakerraspbian/"
        fh = logging.FileHandler(LOGDIR + "coffee.log", mode="w")
        ih = logging.FileHandler(LOGDIR + "important.log")
        fm = logging.Formatter('%(asctime)s:%(name)s: %(message)s')

        fh.setLevel(logging.DEBUG)
        ih.setLevel(logging.WARNING)
        fh.setFormatter(fm)
        ih.setFormatter(fm)

        self.logger = logging.getLogger("main")
        self.logger.addHandler(fh)
        self.logger.addHandler(ih)
        self.logger.setLevel(logging.DEBUG)

        self.logger.debug("Initialized")

        GPIO.setmode(GPIO.BCM)

        # GPIO18 - Coffee Machine
        # GPIO23 - Script Running Status
        # GPIO16 - Load Indicator
        # GPIO12 - Switch
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(23, GPIO.OUT)
        GPIO.setup(16, GPIO.OUT)
        GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Launch Indicator
        GPIO.output(23, GPIO.HIGH)

        # Initialize TwitterChecker
        self.t_checker = TwitterChecker(self.logger)
        self.w_checker = WebChecker(self.logger)

        self.loaded = False
        self.prev_status = GPIO.input(12)

        self.loop()
    
    def make_coffee(self):
        self.loaded = False

        # Turn load indicator off
        GPIO.output(16, GPIO.LOW)

        GPIO.output(18, GPIO.HIGH)

        # Pause for five minutes (or how long it take to make coffee)
        time.sleep(300)
        GPIO.output(18, GPIO.LOW)

        self.prev_status = GPIO.input(12)

    def loop(self):
        while True:
            if self.prev_status != GPIO.input(12):
                print(self.loaded)
                self.loaded = True

            # Set load indicator accordingly
            GPIO.output(16, self.loaded)

            try:
                if self.loaded and (self.t_checker.loop() or self.w_checker.loop()):
                    self.logger.debug("Coffee is being made.")
                    self.make_coffee()
            except KeyboardInterrupt:
                sys.exit()
                self.logger.warning("User interrupted.")
            except:
                self.logger.warning("Twitter limit hit.")
                if self.w_checker.loop():
                    self.logger.debug("Coffee is being made.")
                    self.make_coffee()

            self.prev_status = GPIO.input(12)
            time.sleep(1)


# Clean up
def clean_up():
    GPIO.cleanup()

atexit.register(clean_up)

machine = CoffeeMachine()
