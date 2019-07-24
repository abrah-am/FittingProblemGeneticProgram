
# coding: utf-8

# # Item
# This class represents an object that contains two attributes: 
# Size and Value.



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
