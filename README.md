# FittingProblemGeneticProgram
This repository contains a demo to solve a problem of fitting items into a bucket using both, the programming and generic program approach.

__Description__  
There is a list of items, each item has a size and value attribute. The program needs to select items from the list and try to fit them in a bucket, the bucket has a size limit. The solution to the problem is to find the best selection of items to add the most value to the bucket without exceeding the capacity.

__Programming Approach__  
For the programing approach. There are three easy ways to solve the problem:  
1. Sort the list of items by size and value then add them to the container until it reaches its max capacity.
  With this approach, items with higher size and higher value will be added first.
   
2. Sort the list of items by value and size then add them to the container until it reaches its max capacity.   
  With this approach, items with higher value and higher size will be added first.  

3. Sort the list using a ratio, diving the size by the value, to obtain a more uniform distribution then add them to the container until it reaches its max capacity. 
  With this approach, there will be a more uniform distribution of size and value.
  

