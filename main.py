from twitter import TwitterChecker
from web import WebChecker
import time
from RPi import GPIO

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
    # print("make coffee")

    # Pause for five minutes (or how long it take to make coffee)
    time.sleep(300)
    GPIO.output(5, GPIO.LOW)

while True:
    try:
        if t_checker.loop() or w_checker.loop():
            make_coffee()
    except:
        if w_checker.loop():
            make_coffee()
    time.sleep(1)
