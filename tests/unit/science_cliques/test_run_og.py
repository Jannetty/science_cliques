import unittest
from science_cliques.run_og import run_og


class TestModel(unittest.TestCase):
    def test_run_og(self):
        run_og(False, "test_og.csv")
