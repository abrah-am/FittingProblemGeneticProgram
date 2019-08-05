import unittest

from modules.item_module import *


class TestTraditionalSolution(unittest.TestCase):

    def test_solution_based_on_size_and_value(self):
        item_collection = ItemCollection(items=[Item(10, 7), Item(11, 9), Item(10, 9), Item(12, 9), Item(15, 1), Item(4, 8)])
        expected_collection = ItemCollection(items=[Item(10, 9), Item(11, 9), Item(12, 9), Item(4, 8), Item(10, 7), Item(15, 1)])
        actual_collection = NonGASolutions.by_value_then_size(item_collection)
        self.assertEqual(actual_collection, expected_collection)

    def test_solution_based_on_value_and_size(self):
        item_collection = ItemCollection(items=[Item(10, 7), Item(11, 9), Item(10, 9), Item(10, 8), Item(15, 1), Item(4, 8)])
        expected_collection = ItemCollection(items=[Item(4, 8), Item(10, 9), Item(10, 8), Item(10, 7), Item(11, 9), Item(15, 1)])
        actual_collection = NonGASolutions.by_size_then_value(item_collection)
        self.assertEqual(actual_collection, expected_collection)

    def test_solution_based_on_ratio(self):
        # Ratios: [ 0.7 (10,7), 0.9 (10,9), 0.8 (10,8), 2.0(4,8) ] => [2.0, 0.9, 0.8, 0.7]
        item_collection = ItemCollection(items=[Item(10, 7), Item(10, 9), Item(10, 8), Item(4, 8)])
        expected_collection = ItemCollection(items=[Item(4, 8), Item(10, 9), Item(10, 8), Item(10, 7)])
        actual_collection = NonGASolutions.by_ratio_value_size(item_collection)
        self.assertEqual(actual_collection, expected_collection)


if __name__ == '__main__':
    unittest.main()
