import unittest
import copy

from TheKnapsackProblem.genetic_module import GeneticAlgorithm, CandidateSolution
from TheKnapsackProblem.item_module import ItemCollection, Container


class TestGeneticAlgorithm(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestGeneticAlgorithm, self).__init__(*args, **kwargs)

    def test_findOptimalItems(self):
        item_collection = ItemCollection(40)
        container = Container(100)
        algorithm = GeneticAlgorithm(population_size=1000, crossover_rate=9.5, mutation_rate=0.2)
        solution = algorithm.find_optimal_items(item_collection, container)
        container.fitItems(solution)
        print('Best Solution Found: ', container)

    def test_crossover_results_in_same_size_children(self):
        item_collection = ItemCollection(10)
        container = Container(100)
        parent1 = CandidateSolution(item_collection)
        parent2 = CandidateSolution(item_collection)
        algorithm = GeneticAlgorithm(population_size=10, crossover_rate=0.5)
        child1, child2 = algorithm._crossover(parent1, parent2)
        self.assertEqual(len(child1.get_selected_items()), 10)
        self.assertEqual(len(child2.get_selected_items()), 10)

    def test_mutate_list(self):
        item_collection = ItemCollection(10)
        container = Container(100)
        candidate = CandidateSolution(item_collection)
        original = copy.deepcopy(candidate)
        # mutate every element of the list, pass mutation rate 1 = 100%
        candidate.add_mutation(1)
        for i in range(0, 10):
            self.assertNotEqual(original.get_selected_items()[i][1], candidate.get_selected_items()[i][1])


if __name__ == '__main__':
    unittest.main()