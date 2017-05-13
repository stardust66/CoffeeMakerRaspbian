from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError
import time

class WebChecker():
    def __init__(self, logger):
        self.url = "http://spscoffee.herokuapp.com/brew-request/"
        self.logger = logger

    def post_served(self):
        """Tell the server that the coffee has been served

        Send post request with data served=true
        """
        data = urlencode({ "served":"true" }).encode()
        request = Request(self.url, data)
        print(urlopen(request).read().decode())

    def loop(self):
        """Check the website for status

        If someone presses the brew button on the website, the brew_request
        page will say "yes". If not it'll say "no". This function should
        be called repeatedly in a loop.
        """
        response = urlopen(self.url).read().decode()
        if response == "Yay!":
            # Put information both in log and console
            self.logger.debug("Sending post request to server...")
            print("Sending post request to server...")
            self.post_served()
            print()
            return True
        return False
