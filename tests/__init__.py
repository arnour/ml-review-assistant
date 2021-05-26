import os
import unittest


class TestBase(unittest.TestCase):

    def get_resource(self, name):
        return os.path.join(
            os.path.dirname(__file__),
            "resources",
            name
        )

    def get_resources(self, path):
        return os.path.join(
            os.path.dirname(__file__),
            "resources",
            path
        )

    def list_files(self, path):
        return list(os.scandir(path))

    def assertFilesIn(self, expected_files, path):
        existent_files = list(map(lambda f: f.name, os.scandir(path)))
        self.assertSetEqual(
            set(existent_files),
            set(expected_files),
            'Different files found in {}'.format(path)
        )
