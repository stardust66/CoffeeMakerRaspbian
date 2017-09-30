from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import URLError, HTTPError
from socket import timeout
import time

class WebChecker():
    def __init__(self, logger):
        self.url = "https://spscoffee.herokuapp.com/brew-request/"
        self.logger = logger
        self.logger.debug("Website checker initialized.")

    def post_served(self):
        """Tell the server that the coffee has been served

        Send post request with data served=true
        """
        try:
            data = urlencode({ "served":"true" }).encode()
            request = Request(self.url, data)
            self.logger.debug(urlopen(request).read().decode())
        except HTTPError as e:
            self.logger.error("Couldn't send post request to server.")
            self.logger.error("Server Error: " + e.code)

    def loop(self):
        """Check the website for status

        If someone presses the brew button on the website, the brew_request
        page will say "yes". If not it'll say "no". This function should
        be called repeatedly in a loop.
        """
        # Account for network or server errors
        try:
            response = urlopen(self.url, timeout=10).read().decode()
            if response == "Yay!":
                # Put information both in log and console
                self.logger.debug("Sending post request to server...")
                self.post_served()
                return True
        except URLError as e:
            self.logger.error("URLError: " + e.reason)
        except HTTPError as e:
            self.logger.error("Server Error: " + e.code)
        except timeout:
            self.logger.error("Timeout")
        return False
