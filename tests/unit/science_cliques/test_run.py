import unittest
from science_cliques.run import run


class TestModel(unittest.TestCase):
    def test_run(self):
        run(False, "test_run.csv")
