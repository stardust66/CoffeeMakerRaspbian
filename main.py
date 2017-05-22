#!/usr/bin/env python3

from twitter import TwitterChecker
from web import WebChecker
import time
import logging
import sys
import os
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

# Using GPIO03
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

# Launch Indicator
GPIO.output(23, GPIO.HIGH)

# Initialize TwitterChecker
t_checker = TwitterChecker(logger)
w_checker = WebChecker(logger)

def make_coffee():
    GPIO.output(18, GPIO.HIGH)

    # Pause for five minutes (or how long it take to make coffee)
    time.sleep(300)
    GPIO.output(18, GPIO.LOW)

while True:
    try:
        if t_checker.loop() or w_checker.loop():
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
    time.sleep(1)
