import tweepy
import time
import datetime
import os
import sys

allowed_users = ["jasonchen66", "s0rokka"]

class TwitterChecker():
    def __init__(self, logger):
        # Authentication
        try:
            auth1 = os.environ["AUTH_HANDLE1"]
            auth2 = os.environ["AUTH_HANDLE2"]
            access1 = os.environ["ACCESS1"]
            access2 = os.environ["ACCESS2"]
        except:
            logger.error("Twitter authentication failed.")
            logger.error("Exiting!")
            sys.exit()

        auth = tweepy.OAuthHandler(auth1, auth2)
        auth.set_access_token(access1, access2)
        self.api = tweepy.API(auth)
        self.last_checked = (datetime.datetime.now()
                             - datetime.timedelta(seconds=15))
        self.logger = logger

    def loop(self):
        """Use API to search, view, or post tweets"""
        if (self.last_checked
            < datetime.datetime.now() - datetime.timedelta(seconds=15)):

            delta = (datetime.datetime.now()
                    - datetime.timedelta(seconds=40, minutes=4))

            self.last_checked = datetime.datetime.now()
            search = self.api.search("#spscoffee2k17")
            if search:
                first_post = search[0]

                # Correct for timezone
                # Only works for EDT
                eastern = datetime.timedelta(hours=4)
                first_post.created_at -= eastern

                # Check if the post is made within five minutes
                if (self._validate_post(first_post)):
                    self.logger.debug("Found tweet.")

                    text = first_post.text
                    username = first_post.user.screen_name

                    self.logger.debug("Text: " + text)
                    self.logger.debug("Username: " + username)
                    print(text)
                    print(username)
                    print()
                    return True
                else:
                    print("None within five minutes")
            else:
                print("None")
                return False
        print("It hasn't been 15 seconds yet")
        return False

    def _validate_post(self, post):
        allowed_users = ["jasonchen66", "s0rokka"]
        delta = (datetime.datetime.now()
                - datetime.timedelta(seconds=40, minutes=4))

        if (post.created_at > delta and
                post.user.screen_name in allowed_users):
            return True
        else:
            return False

