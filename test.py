import unittest
import datetime
import os

from twitter import TwitterChecker

class PassLogger():
    def debug(self, message):
        pass

    def warning(self, message):
        pass

    def error(self, message):
        pass

class TestUser():
    def __init__(self, name):
        self.screen_name = name

class TestPost():
    def __init__(self, username, created_at):
        self.user = TestUser(username)
        self.created_at = created_at

class TestTwitterChecker(unittest.TestCase):
    def setUp(self):

        os.environ["AUTH_HANDLE1"] = "test"
        os.environ["AUTH_HANDLE2"] = "test"
        os.environ["ACCESS1"] = "test"
        os.environ["ACCESS2"] = "test"

        self.logger = PassLogger()
        self.t_checker = TwitterChecker(self.logger)
        time_now = datetime.datetime.utcnow()
        wrong_time = time_now - datetime.timedelta(hours=4)
        self.right_post = TestPost("jasonchen66", time_now)
        self.wrong_username = TestPost("hello", time_now)
        self.wrong_time = TestPost("jasonchen66", wrong_time)

    def test_right_post(self):
        self.assertTrue(self.t_checker._validate_post(self.right_post))

    def test_wrong_user(self):
        self.assertFalse(self.t_checker._validate_post(self.wrong_username))

    def test_wrong_time(self):
        self.assertFalse(self.t_checker._validate_post(self.wrong_time))

if __name__ == "__main__":
    unittest.main()
