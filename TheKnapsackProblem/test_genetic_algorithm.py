import unittest
import copy

from genetic_module import GeneticAlgorithm, CandidateSolution
from item_module import *


class TestGeneticAlgorithm(unittest.TestCase):

    def setUp(self):
        self.selected_items1 = [[Item(10, 10), True], [Item(20, 20), True], [Item(30, 30), True],
                                [Item(40, 40), True], [Item(50, 50), True]]
        self.selected_items2 = [[Item(600, 60), True], [Item(70, 70), True], [Item(80, 80), True],
                                [Item(90, 90), True], [Item(100, 100), True]]

    def __init__(self, *args, **kwargs):
        super(TestGeneticAlgorithm, self).__init__(*args, **kwargs)

    def test_findOptimalItems(self):
        item_collection = ItemCollection(40)
        container = Container(100)
        solution = GeneticAlgorithm.find_optimal_items(item_collection=item_collection, container=container,
                                                       population_size=100, crossover_rate=9.0, mutation_rate=0.0)
        container.fit_items(solution)
        self.assertLessEqual(container.get_total_size(), 100, 'The container should have less than 100')

    def test_crossover_with_zero_crossover_rate(self):
        parent1 = CandidateSolution(selected_items=self.selected_items1)
        parent2 = CandidateSolution(selected_items=self.selected_items2)

        child1, child2 = GeneticAlgorithm.crossover(parent1=parent1, parent2=parent2, crossover_rate=0.0)

        self.assertEqual(parent1, child1, 'Parent and Child should be identical')
        self.assertEqual(parent2, child2, 'Parent and Child should be identical')

    def test_crossover_with_crossover_rate(self):
        parent1 = CandidateSolution(selected_items=self.selected_items1)
        parent2 = CandidateSolution(selected_items=self.selected_items2)

        child1, child2 = GeneticAlgorithm.crossover(parent1=parent1, parent2=parent2, crossover_rate=1.0)

        self.assertNotEqual(parent1, child1, 'Parent and Child should NOT be identical')
        self.assertNotEqual(parent2, child2, 'Parent and Child should NOT be identical')

    def test_mutate_candidate_with_mutation_rate(self):
        selected_items = copy.deepcopy(self.selected_items1)
        candidate = CandidateSolution(selected_items=selected_items)
        candidate.add_mutation(1.0)
        self.assertNotEqual(self.selected_items1, candidate.get_selected_items())

    def test_mutate_candidate_without_mutation_rate(self):
        selected_items = copy.deepcopy(self.selected_items1)
        candidate = CandidateSolution(selected_items=selected_items)
        candidate.add_mutation(0.0)
        self.assertEqual(self.selected_items1, candidate.get_selected_items())


if __name__ == '__main__':
    unittest.main()
