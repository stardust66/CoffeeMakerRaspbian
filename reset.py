from RPi import GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

GPIO.output(23, GPIO.LOW)
GPIO.output(18, GPIO.LOW)

# Clean up
GPIO.cleanup()
