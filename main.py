import twitter
import web
import time

while True:
    twitter.loop()
    web.loop()
    time.sleep(1)
