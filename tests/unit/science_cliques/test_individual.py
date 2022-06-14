import unittest
from science_cliques.individual import get_ties, \
    check_get_max_n_indices_params, get_max_n_indices

class TestIndividual(unittest.TestCase):

    def test_get_ties_works(self):
        list = [5,7,9,2,4,5,6,7,5]
        expected_idx = [0, 5, 8]
        return_idx = get_ties(list, 5)
        assert(return_idx == expected_idx)

    def test_get_ties_can_return_empty(self):
        list = [5,7,9,2,11,5,6,7,5]
        i = 4
        expected_idx = [i]
        return_idx = get_ties(list, list[i])
        assert(return_idx == expected_idx)

    def test_check_get_max_n_indices_params(self):
        # list has non-float
        list = [0, 4, "hey", 9]
        n = 1
        with self.assertRaises(ValueError):
            check_get_max_n_indices_params(list, n)
        # n < 1
        list = [0, 4, 6, 9]
        n = -1
        with self.assertRaises(ValueError):
            check_get_max_n_indices_params(list, n)
        # len(list) < 1
        list = []
        n = 1
        with self.assertRaises(ValueError):
            check_get_max_n_indices_params(list, n)
        # n > len(list)
        list = [10, 2, 4]
        n = 4
        with self.assertRaises(ValueError):
            check_get_max_n_indices_params(list, n)
        n = 2
        # should work
        assert(check_get_max_n_indices_params(list, n) is None)

    def test_get_max_n_indices(self):
        n = 2
        list = [9, 3, 7, 9, 9, 6, 9, 10]
        assert(len(get_max_n_indices(list, n)) == n)