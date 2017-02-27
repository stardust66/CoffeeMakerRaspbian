from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError
import time

def post_served():
    """Tell the server that the coffee has been served

    Send post request with data served=true
    """
    url = "http://spscoffee.herokuapp.com/brew-request/"
    url = "http://localhost:8000/brew-request/"

    data = urlencode({ "served":"true" }).encode()
    request = Request(url, data)
    print(urlopen(request).read().decode())

def loop():
    """Check the website for status

    If someone presses the brew button on the website, the brew_request
    page will say "yes". If not it'll say "no". This function should
    be called repeatedly in a loop.
    """
    url = "http://spscoffee.herokuapp.com/brew-request/"
    url = "http://localhost:8000/brew-request/"

    response = urlopen(url).read().decode()
    if response == "Yay!":
        print("make coffee")
        print()
        print("Sending post request to server...")
        post_served()
        print()

while True:
    loop()
    time.sleep(0.1)
