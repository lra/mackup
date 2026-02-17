import unittest
from unittest.mock import patch

from mackup import constants


class TestConstants(unittest.TestCase):
    def test_get_version_returns_metadata_version(self):
        with patch("mackup.constants.version", return_value="1.2.3"):
            self.assertEqual(constants._get_version(), "1.2.3")

    def test_get_version_falls_back_when_metadata_missing(self):
        with patch(
            "mackup.constants.version",
            side_effect=constants.PackageNotFoundError("mackup"),
        ):
            self.assertEqual(constants._get_version(), "unknown")
