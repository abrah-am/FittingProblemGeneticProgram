import unittest

from TheKnapsackProblem.genetic_module import GeneticAlgorithm, CandidateSolution
from TheKnapsackProblem.item_module import ItemCollection, Container


class TestCandidate(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCandidate, self).__init__(*args, **kwargs)

    def test_candidateSize(self):
        itemCol = ItemCollection(20)
        container = Container(100)
        candidate = CandidateSolution(itemCol)
        self.assertEqual(len(itemCol.get_items()), len(candidate.get_selected_items()))

    def test_repairCandidate(self):
        itemCol = ItemCollection(20)
        container = Container(100)
        candidate = CandidateSolution(itemCol)
        candidate.repair(container)
        self.assertLessEqual(candidate.get_size_of_selected(), container.get_capacity())


if __name__ == '__main__':
    unittest.main()