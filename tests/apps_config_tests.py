import os
import tempfile
import unittest
import stat

try:
    from unittest.mock import patch
except ImportError:
    patch = None


from mackup import utils
from mackup.appsdb import ApplicationsDatabase


realpath = os.path.dirname(os.path.realpath(__file__))
APPLICATIONS_DIR = os.path.join(realpath, "..", "mackup", "applications")
FIXTURES_DIR = os.path.join(realpath, "fixtures")


class TestMackup(unittest.TestCase):
    config_file_path = os.path.join(APPLICATIONS_DIR, "test-app.cfg")

    def setUp(self):
        os.environ["HOME"] = FIXTURES_DIR

        with open(self.config_file_path, "w", encoding='utf-8') as config_file:
            config_file.write(
                "\n".join(
                    [
                        "[application]",
                        "name = Test App",
                        "",
                        "[options]",
                        "enable_glob = true",
                        "",
                        "[configuration_files]",
                        "Library/Application Support/Test App/*/data.txt",
                    ]
                )
            )

    def tearDown(self):
        os.remove(self.config_file_path)

    def test_glob_configuration_paths(self):
        if patch:
            with patch.object(
                ApplicationsDatabase,
                "get_config_files",
                return_value=[self.config_file_path],
            ) as method:
                app_db = ApplicationsDatabase()
                self.assertEqual(
                    app_db.get_files("test-app"),
                    {
                        "Library/Application Support/Test App/2020/data.txt",
                        "Library/Application Support/Test App/2021/data.txt",
                        "Library/Application Support/Test App/2022/data.txt",
                    },
                )
        else:
            app_db = ApplicationsDatabase()
            app_db.get_config_files = lambda *args, **kwargs: [self.config_file_path]
            self.assertEqual(
                app_db.get_files("test-app"),
                {
                    "Library/Application Support/Test App/2020/data.txt",
                    "Library/Application Support/Test App/2021/data.txt",
                    "Library/Application Support/Test App/2022/data.txt",
                },
            )
