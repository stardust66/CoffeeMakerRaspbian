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
        self.LOGDIR = "/home/pi/Documents/coffeemakerraspbian/"
        fh = logging.FileHandler(self.LOGDIR + "coffee.log")
        ih = logging.FileHandler(self.LOGDIR + "important.log")
        ch = logging.StreamHandler(sys.stdout)
        fm = logging.Formatter('%(asctime)s:%(name)s: %(message)s')
        sm = logging.Formatter('%(message)s')

        fh.setLevel(logging.DEBUG)
        ih.setLevel(logging.WARNING)
        ch.setLevel(logging.DEBUG)
        fh.setFormatter(fm)
        ih.setFormatter(fm)
        ch.setFormatter(sm)

        self.logger = logging.getLogger("main")
        self.logger.addHandler(fh)
        self.logger.addHandler(ih)
        self.logger.addHandler(ch)
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

        # Read loaded from file
        try:
            with open(self.LOGDIR + "loaded.state", mode="r") as f:
                val = f.readline()
                if val is not None and "True" in val:
                    self.loaded = True
                    self.logger.debug("Loaded set to True from file.")
                else:
                    self.loaded = False
                    print("Loaded set to False from file.")
        except FileNotFoundError:
            self.logger.debug("File not found.")
            self.loaded = False

        self.prev_status = GPIO.input(12)

        self.loop()
    
    def change_loaded(self, loaded):
        self.loaded = loaded
        self.logger.debug("Loaded is set to " + str(self.loaded))
        with open(self.LOGDIR + "loaded.state", mode="w+") as f:
            f.write(str(self.loaded))

    def make_coffee(self):
        self.change_loaded(False)

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
                self.change_loaded(True)

            # Set load indicator accordingly
            GPIO.output(16, self.loaded)

            try:
                if self.loaded and (self.t_checker.loop() or self.w_checker.loop()):
                    self.logger.debug("Coffee is being made.")
                    self.make_coffee()
            except KeyboardInterrupt:
                sys.exit()
                self.logger.error("User interrupted.")
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
