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

# Configure Log
LOGDIR = "/home/pi/Documents/coffeemakerraspbian/"
logger = logging.getLogger("main")
fh = logging.FileHandler(LOGDIR + "coffee.log", mode="w")
ih = logging.FileHandler(LOGDIR + "important.log")
fm = logging.Formatter('%(asctime)s:%(name)s: %(message)s')

fh.setLevel(logging.DEBUG)
ih.setLevel(logging.WARNING)
fh.setFormatter(fm)
ih.setFormatter(fm)

logger = logging.getLogger("main")
logger.addHandler(fh)
logger.addHandler(ih)
logger.setLevel(logging.DEBUG)

logger.debug("Initialized")

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
t_checker = TwitterChecker(logger)
w_checker = WebChecker(logger)

loaded = False
prev_status = GPIO.input(12)

# Clean up
def clean_up():
    GPIO.cleanup()

atexit.register(clean_up)

def make_coffee():
    loaded = False

    # Turn load indicator off
    GPIO.output(16, GPIO.LOW)

    GPIO.output(18, GPIO.HIGH)

    # Pause for five minutes (or how long it take to make coffee)
    time.sleep(300)
    GPIO.output(18, GPIO.LOW)

    prev_status = GPIO.input(12)

while True:
    if prev_status != GPIO.input(12):
        loaded = True

    # Set load indicator accordingly
    GPIO.output(16, loaded)

    try:
        if loaded and (t_checker.loop() or w_checker.loop()):
            logger.debug("Coffee is being made.")
            make_coffee()
    except KeyboardInterrupt:
        sys.exit()
        logger.warning("User interrupted.")
    except:
        logger.warning("Twitter limit hit.")
        if w_checker.loop():
            logger.debug("Coffee is being made.")
            make_coffee()

    prev_status = GPIO.input(12)
    time.sleep(1)

