from twitter import TwitterChecker
from web import WebChecker
import time
import logging
import sys
from RPi import GPIO

# Configure Log
logging.basicConfig(format='%(asctime)s:%(name)s: %(message)s',
                    filename="coffee.log", level=logging.WARNING)
logger = logging.getLogger("script")
logger.setLevel(logging.DEBUG)

GPIO.setmode(GPIO.BOARD)

# Using GPIO03
GPIO.setup(5, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)

# Launch Indicator
GPIO.output(7, GPIO.HIGH)

# Initialize TwitterChecker
t_checker = TwitterChecker(logger)
w_checker = WebChecker(logger)

def make_coffee():
    GPIO.output(5, GPIO.HIGH)

    # Pause for five minutes (or how long it take to make coffee)
    time.sleep(300)
    GPIO.output(5, GPIO.LOW)

while True:
    try:
        if t_checker.loop() or w_checker.loop():
            logging.debug("Coffee is being made.")
            make_coffee()
    except KeyboardInterrupt:
        sys.exit()
        logging.warning("User interrupted.")
    except:
        logging.warning("Twitter limit hit.")
        if w_checker.loop():
            logging.debug("Coffee is being made.")
            make_coffee()
    time.sleep(1)
