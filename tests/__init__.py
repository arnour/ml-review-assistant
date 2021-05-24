import os
import unittest


class TestBase(unittest.TestCase):

    def get_resource(self, name):
        return os.path.join(
            os.path.dirname(__file__),
            "resources",
            name
        )
