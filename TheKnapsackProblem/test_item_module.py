import unittest
from item_module import Item, ItemCollection


class TestItemModule(unittest.TestCase):

    def test_createItem(self):
        item = Item(10, 20)
        self.assertEqual(item.getSize(), 10)
        self.assertEqual(item.getValue(), 20)

    def test_ItemCollection_getItems(self):
        item_col = ItemCollection(10)
        self.assertEqual(len(item_col.getItems()), 10)


if __name__ == '__main__':
    unittest.main()
