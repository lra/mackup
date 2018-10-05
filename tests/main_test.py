import unittest
from mackup import main


class TestMain(unittest.TestCase):

    def test_main_header(self):
        assert main.header('blah') == '\033[34mblah\033[0m'

    def test_main_bold(self):
        assert main.bold('blah') == '\033[1mblah\033[0m'
