import unittest

from modules.genetic_module import *


class TestCandidate(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCandidate, self).__init__(*args, **kwargs)

    def test_candidateSize(self):
        container = Container(100)
        candidate = CandidateSolution(selected_items=[[Item(10, 10), True], [Item(20, 20), True],
                                                      [Item(30, 30), True], [Item(40, 40), True],
                                                      [Item(50, 50), True]])
        self.assertGreaterEqual(candidate.get_size_of_selected(), container.get_capacity())
        candidate.repair(container)
        self.assertLessEqual(candidate.get_size_of_selected(), container.get_capacity())


if __name__ == '__main__':
    unittest.main()