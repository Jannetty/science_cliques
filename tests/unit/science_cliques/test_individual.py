import unittest
from science_cliques.individual import (
    get_ties,
    check_get_max_n_indices_params,
    get_max_n_indices,
    i_is_first_element,
)
from science_cliques.model import CliqueModel


class TestIndividual(unittest.TestCase):
    def test_get_ties_works(self):
        list = [5, 7, 9, 2, 4, 5, 6, 7, 5]
        expected_idx = [0, 5, 8]
        return_idx = get_ties(list, 5)
        assert return_idx == expected_idx

    def test_get_ties_can_return_empty(self):
        list = [5.0, 7.0, 9.0, 2.0, 11.0, 5.0, 6.0, 7.0, 5.0]
        i = 4
        expected_idx = [i]
        return_idx = get_ties(list, list[i])
        assert return_idx == expected_idx

    def test_check_get_max_n_indices_params(self):
        # list has non-float
        list = [0.0, 4.0, "hey", 9.0]
        n = 1
        with self.assertRaises(ValueError):
            check_get_max_n_indices_params(list, n)
        # n < 1
        list = [0.0, 4.0, 6.0, 9.0]
        n = -1
        with self.assertRaises(ValueError):
            check_get_max_n_indices_params(list, n)
        # len(list) < 1
        list = []
        n = 1
        with self.assertRaises(ValueError):
            check_get_max_n_indices_params(list, n)
        # n > len(list)
        list = [10.0, 2.0, 4.0]
        n = 4
        with self.assertRaises(ValueError):
            check_get_max_n_indices_params(list, n)
        n = 2
        # should work
        assert check_get_max_n_indices_params(list, n) is None

    def test_get_max_n_indices(self):
        n = 2
        list = [9.0, 3.0, 7.0, 9.0, 9.0, 6.0, 9.0, 10.0]
        assert len(get_max_n_indices(list, n)) == n

    def test_i_is_first_element(self):
        assert i_is_first_element(0)

    def test_get_random_index_beliefs(self):
        model = CliqueModel(skeptical=True)
        agent0_abstained_belief = model.schedule._agents[0].get_random_index_of_abstained_belief()
        assert model.schedule._agents[0].all_facts[agent0_abstained_belief] == 0
        agent0_not_abstained_belief = model.schedule._agents[
            0
        ].get_random_index_of_not_abstained_belief()
        assert model.schedule._agents[0].all_facts[agent0_not_abstained_belief] != 0

    def test_offer_testimony(self):
        model = CliqueModel(skeptical=True)
        agent0 = model.schedule._agents[0]
        return_tuple = agent0.offer_testimony()
        assert return_tuple[1] != 0

    def test_step(self):
        model = CliqueModel(skeptical=True)
        agent0 = model.schedule._agents[0]
        agent0.step()
