import random

# This class represents an object that contains two attributes: 
class Item:
    def __init__(self, size, value):
        self.size = size
        self.value = value
        
    def getSize(self):
        return self.size
    
    def getValue(self):
        return self.value
    
    def __str__(self):
        return '[s={};v={}]'.format(self.size, self.value)
    
    def __repr__(self):
        return '[s={};v={}]'.format(self.size, self.value)


# This class represents a collection of items with sorting methods
class ItemCollection:
    def __init__(self, noOfItems=10, size=(1, 100), value=(1,100)):
        self.items = self._generateRandomItems(noOfItems, size, value)
        
    def getItems(self):
        return self.items
    
    def _generateRandomItems(self, noOfItems=10, size=(1, 100), value=(1,100)):
        result = []
        for i in range(noOfItems):
            result.append(Item(
                random.randint(size[0],size[1]), 
                random.randint(size[0],size[1])))
        return result
    
    def sortBySize(self):
        self.items = sorted(self.items, key=lambda x: (x.getSize(), x.getValue()), reverse=True)
    
    def sortByValue(self):
        self.items = sorted(self.items, key=lambda x: (x.getValue(), x.getSize()), reverse=True)
    
    def sortByRatio(self):
        self.items = sorted(self.items, key=lambda x: (x.getValue() / x.getSize()), reverse=True)
    
    def __repr__(self):
        return self.__str__()
        
    def __str__(self):
        response = ''
        for item in self.getItems():
            response += str(item) + '\t'
        return response


# This class represents a container to place items in.
class Container:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
    
    def setItems(self, items):
        self.items = items
        
    def getItems(self):
        return self.items
    
    def getCapacity(self):
        return self.capacity
    
    def getTotalSize(self):
        if len(self.items) > 0:
            return sum(i.getSize() for i in  self.items)
        else:
            return 0
    
    def fitItems(self, itemCollection):
        self.items = []
        sizeUsed=0
        for item in itemCollection.getItems():
            if((sizeUsed + item.getSize()) <= self.capacity):
                self.items.append(item)
                sizeUsed += item.getSize()
    
    def getTotalValue(self):
        if len(self.items) > 0:
            return sum(i.getValue() for i in  self.items)
        else:
            return 0
        
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return 'Items:{}\nTotal Occupied Size:{}\nTotal Value:{}'.format(
            self.getItems(), self.getTotalSize(), self.getTotalValue())
