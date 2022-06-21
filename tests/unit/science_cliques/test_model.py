import unittest
from science_cliques.model import calculate_default_reliability, check_model_init_params
from science_cliques.model import CliqueModel


class TestModel(unittest.TestCase):
    def test_calculate_default_reliability(self):
        reliabilities = []
        for i in range(100):
            reliabilities.append(calculate_default_reliability())
        average_reliability = sum(reliabilities) / len(reliabilities)
        assert abs(average_reliability - 0.6) < 1

    def test_check_model_init_params(self):
        with self.assertRaises(ValueError):
            # no philosophy selected
            check_model_init_params(
                number_of_individuals=100,
                number_of_neighbors=8,
                num_facts=1500,
                starting_knowledge=15,
                skeptical=False,
                reid=False,
                direct=False,
                indirect=False,
            )
        with self.assertRaises(ValueError):
            # multiple philosophies selected
            check_model_init_params(
                number_of_individuals=100,
                number_of_neighbors=8,
                num_facts=1500,
                starting_knowledge=15,
                skeptical=True,
                reid=True,
                direct=False,
                indirect=False,
            )
        with self.assertRaises(ValueError):
            # more starting facts than facts
            check_model_init_params(
                number_of_individuals=100,
                number_of_neighbors=8,
                num_facts=14,
                starting_knowledge=15,
                skeptical=True,
                reid=False,
                direct=False,
                indirect=False,
            )
        with self.assertRaises(ValueError):
            # more neighbors than individuals
            check_model_init_params(
                number_of_individuals=6,
                number_of_neighbors=8,
                num_facts=1500,
                starting_knowledge=15,
                skeptical=True,
                reid=False,
                direct=False,
                indirect=False,
            )

    def test_step(self):
        model = CliqueModel(skeptical=True)
        model.step()
        model = CliqueModel(reid=True)
        model.step()
        model = CliqueModel(direct=True)
        model.step()
        model = CliqueModel(indirect=True)
        model.step()
