import unittest

from science_cliques.runshort import run_short


class TestModel(unittest.TestCase):
    def test_run_short(self):
        run_short()
