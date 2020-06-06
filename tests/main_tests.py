import unittest
from mackup import main
from mackup.colorize import (
    colorize_text,
    colorize_filename,
    colorize_name,
    colorize_item_bullet,
    colorize_header,
    colorize_header_app_name,
)


class TestMain(unittest.TestCase):
    def test_colorize_text(self):
        assert colorize_text("Blah") == "\x1b[1;33mBlah\x1b[0m"

    def test_colorize_filename(self):
        assert colorize_filename("Blah") == "\x1b[1;34mBlah\x1b[0m"

    def test_colorize_name(self):
        assert colorize_name("Blah") == "\x1b[1;34mBlah\x1b[0m"

    def test_colorize_item_bullet(self):
        assert colorize_item_bullet("Blah") == "\x1b[1;32mBlah\x1b[0m"

    def test_colorize_header(self):
        assert colorize_header("Blah") == "\x1b[1;35mBlah\x1b[0m"

    def test_colorize_header_app_name(self):
        assert colorize_header_app_name("Blah") == "\x1b[1;34mBlah\x1b[0m"
