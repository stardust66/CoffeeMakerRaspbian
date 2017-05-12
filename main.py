from twitter import TwitterChecker
import web
import time
from RPi import GPIO

GPIO.setmode(GPIO.BOARD)

# Using GPIO03
GPIO.setup(5, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)

# Launch Indicator
GPIO.output(7, GPIO.HIGH)

# Initialize TwitterChecker
checker = TwitterChecker()

def make_coffee():
    GPIO.output(5, GPIO.HIGH)
    # print("make coffee")

    # Pause for five minutes (or how long it take to make coffee)
    time.sleep(300)
    GPIO.output(5, GPIO.LOW)

while True:
    try:
        if checker.loop() or web.loop():
            make_coffee()
    except:
        if web.loop():
            make_coffee()
    time.sleep(1)
