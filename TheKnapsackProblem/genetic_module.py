import random
import copy
import sys
from item_module import ItemCollection, Container, Item

class CandidateSolution:
    """
    Candidate Solution: This class represents a potential solution. It receives the list of items and
    it assigns a True or False value to each item. True means that it is selected.
    It contains a method to adjust the candidate if it exceeds the container's capacity.
    """
    def __init__(self, item_collection=None, selected_items=None):
        if selected_items is None:
            self.selected_items = CandidateSolution.get_random_selection(item_collection)
        else:
            self.selected_items = selected_items

    @staticmethod
    def get_random_selection(item_collection):
        return [[item, bool(random.getrandbits(1))]
                for item in item_collection.getItems()]

    def get_selected_items(self):
        return self.selected_items

    def get_size_of_selected(self):
        return sum((selected[0].getSize() if selected[1] else 0)
                   for selected in self.selected_items)

    def get_value_of_selected(self):
        return sum((selected[0].getValue() if selected[1] else 0)
                   for selected in self.selected_items)

    def repair(self, container):
        while self.get_size_of_selected() > container.getCapacity():
            check = random.randint(0, len(self.selected_items) - 1)
            if self.selected_items[check][1]:
                self.selected_items[check][1] = False

    def add_mutation(self, mutation_rate):
        for selected in self.selected_items:
            if random.uniform(0, 1) < mutation_rate:
                selected[1] = not selected[1]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        to_string = '\nCandidateSolution: \n'
        for selected in self.selected_items:
            to_string += '{};\n'.format(selected)
        to_string += 'Calculated Fitness: {}\nCalculated Value: {}'.format(
            self.get_size_of_selected(), self.get_value_of_selected())
        return to_string


class GeneticAlgorithm:
    MAX_GENERATION_WITHOUT_CHANGE = 10

    """
    Genetic Algorithm: This class contains the implementation of the genetic algorithm.
    """
    def __init__(self, population_size=0, crossover_rate=0, mutation_rate=0):
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.population = []

    def find_optimal_items(self, item_collection, container):
        # 1. Population
        self.population = [CandidateSolution(item_collection)
                           for i in range(self.population_size)]

        best_fitness_score_all_time = -sys.maxsize-1
        best_solution_all_time = None
        generation_number = 1
        while True:
            total_fitness = 0
            best_fitness_score_in_this_generation = -sys.maxsize-1
            best_solution_in_this_generation = None

            # 2. Selection.
            # 2.1 Fitness evaluation
            for candidate in self.population:
                candidate.repair(container)
                total_fitness += candidate.get_value_of_selected()
                # 2.2 Find best candidate in this generation
                if candidate.get_value_of_selected() > best_fitness_score_in_this_generation:
                    best_fitness_score_in_this_generation = candidate.get_value_of_selected()
                    best_solution_in_this_generation = copy.deepcopy(candidate)

            # 2.3 Compare with previous candidates
            if best_fitness_score_in_this_generation > best_fitness_score_all_time:
                best_fitness_score_all_time = best_fitness_score_in_this_generation
                best_solution_all_time = best_solution_in_this_generation
                best_solution_generation_number = generation_number
            # 2.4 Stop when it stopped changing.
            elif generation_number - best_solution_generation_number > self.MAX_GENERATION_WITHOUT_CHANGE:
                break

            # 2.2 Create the next generation (Mating Pool)
            next_generation = []
            while len(next_generation) < self.population_size:
                # 3 Reproduction
                # 3.1 Select parents
                parent1 = self._select_candidate(total_fitness)
                parent2 = self._select_candidate(total_fitness)

                # 3.2 Crossover
                child1, child2 = self._crossover(parent1, parent2)

                # 3.3 Add Mutation
                child1.add_mutation(self.mutation_rate)
                child2.add_mutation(self.mutation_rate)

                next_generation.append(child1)
                next_generation.append(child2)

            # The new generation becomes the population.
            self.population = next_generation
            generation_number += 1
        return self.to_item_collection(best_solution_all_time)

    @staticmethod
    def to_item_collection(candidate):
        items = []
        for item in candidate.get_selected_items():
            if item[1]:
                items.append(item[0])
        return ItemCollection(items=items)

    def _select_candidate(self, total_fitness):
        """
        This method selects the best fit candidates using the Roulette Wheel Selection method.
        :param total_fitness: The total fitness of all candidates
        :return: Returns a random candidate. A candidate with better fitness scores have a better
        chance of being selected.
        """
        random_value = random.randint(0, total_fitness)
        for candidate in self.population:
            random_value -= candidate.get_value_of_selected()
            if random_value <= 0:
                return candidate
        return self.population[-1]

    def _crossover(self, parent1, parent2):
        """
        This method cross overs two parents to create a new generation.
        Randomly choose an index point and copy from 0 to index from parent one and from index to end from parent two
        This creates a new child.
        :param parent1: One of the candidates selected to be a parent.
        :param parent2: Another parent selected to be a parent.
        :return: A tuple of child1 and child2
        """
        if random.uniform(0, 1) < self.crossover_rate:
            crossover = random.randint(0, len(parent1.get_selected_items()))
            selected_items1 = parent1.get_selected_items()[:crossover] + parent2.get_selected_items()[crossover:]
            selected_items2 = parent2.get_selected_items()[:crossover] + parent1.get_selected_items()[crossover:]
            return CandidateSolution(selected_items=selected_items1), CandidateSolution(selected_items=selected_items2)
        else:
            return copy.deepcopy(parent1), copy.deepcopy(parent2)