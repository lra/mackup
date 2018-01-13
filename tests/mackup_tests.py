import unittest
from mackup import mackup

class TestMackup(unittest.TestCase):

    def Test_mackup_header(self):
        assert mackup.header('blah') == '\033[34mblah\033[0m'

    def test_main_bold(self):
        assert mackup.bold('blah') == '\033[1mblah\033[0m'
