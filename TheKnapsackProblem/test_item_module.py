import unittest
from TheKnapsackProblem.item_module import *


class TestItemModule(unittest.TestCase):

    def test_createItem(self):
        item = Item(10, 20)
        self.assertEqual(item.get_size(), 10)
        self.assertEqual(item.get_value(), 20)

    def test_ItemCollection_getItems(self):
        item_col = ItemCollection(10)
        self.assertEqual(len(item_col.get_items()), 10)


if __name__ == '__main__':
    unittest.main()
