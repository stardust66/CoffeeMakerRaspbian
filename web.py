from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError
import time

url = "http://spscoffee.herokuapp.com/brew-request/"
# url = "http://localhost:8000/brew-request/"

def post_served(url):
    """Tell the server that the coffee has been served

    Send post request with data served=true
    """
    data = urlencode({ "served":"true" }).encode()
    request = Request(url, data)
    print(urlopen(request).read().decode())

def loop():
    """Check the website for status

    If someone presses the brew button on the website, the brew_request
    page will say "yes". If not it'll say "no". This function should
    be called repeatedly in a loop.
    """
    response = urlopen(url).read().decode()
    if response == "Yay!":
        print("Sending post request to server...")
        post_served(url)
        print()
        return True
    return False
