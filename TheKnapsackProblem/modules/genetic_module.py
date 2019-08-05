import copy
import random
import sys

from modules.item_module import *


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
            self.selected_items = CandidateSolution.copy_selected_items(selected_items)
        self.selected_size = self._calculate_selected_size()
        self.selected_value = self._calculate_selected_value()

    @staticmethod
    def copy_selected_items(selected_items):
        return [[Item(item[0].get_size(), item[0].get_value()), item[1]] for item in selected_items]

    @staticmethod
    def get_random_selection(item_collection):
        return [[Item(item.get_size(), item.get_value()), bool(random.getrandbits(1))]
                for item in item_collection.get_items()]

    def get_selected_items(self):
        return self.selected_items

    def _calculate_selected_size(self):
        return sum((selected[0].get_size() if selected[1] else 0)
                   for selected in self.selected_items)

    def _calculate_selected_value(self):
        return sum((selected[0].get_value() if selected[1] else 0)
                   for selected in self.selected_items)

    def get_size_of_selected(self):
        return self.selected_size

    def get_value_of_selected(self):
        return self.selected_value

    def repair(self, container):
        while self.selected_size > container.get_capacity():
            item = random.choice(self.selected_items)
            if item[1]:
                item[1] = False
                self.selected_size = self._calculate_selected_size()
                self.selected_value = self._calculate_selected_value()

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

    def __eq__(self, other):
        if len(self.selected_items) != len(other.selected_items):
            return False
        for i in range(len(self.selected_items)):
            if self.selected_items[i][1] != other.selected_items[i][1] \
                    or self.selected_items[i][0] != other.selected_items[i][0]:
                return False
        return True


class GeneticAlgorithm:
    MAX_GENERATION_WITHOUT_CHANGE = 10

    @staticmethod
    def find_optimal_items(item_collection, container, population_size=1, crossover_rate=0.0, mutation_rate=0.0):
        # 1. Population
        population = [CandidateSolution(item_collection)
                      for i in range(population_size)]

        best_fitness_score_all_time = -sys.maxsize - 1
        best_solution_all_time = None
        generation_number = 1
        while True:
            total_fitness = 0
            best_fitness_score_in_this_generation = -sys.maxsize - 1
            best_solution_in_this_generation = None

            # 2. Selection.
            # 2.1 Fitness evaluation
            for candidate in population:
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
            elif generation_number - best_solution_generation_number > GeneticAlgorithm.MAX_GENERATION_WITHOUT_CHANGE:
                break

            # 2.2 Create the next generation (Mating Pool)
            next_generation = []
            while len(next_generation) < population_size:
                # 3 Reproduction
                # 3.1 Select parents
                parent1 = GeneticAlgorithm._select_candidate(population, total_fitness)
                parent2 = GeneticAlgorithm._select_candidate(population, total_fitness)

                # 3.2 Crossover
                child1, child2 = GeneticAlgorithm.crossover(parent1, parent2, crossover_rate)

                # 3.3 Add Mutation
                child1.add_mutation(mutation_rate)
                child2.add_mutation(mutation_rate)

                next_generation.append(child1)
                next_generation.append(child2)

            # The new generation becomes the population.
            population = next_generation
            generation_number += 1
        return GeneticAlgorithm.to_item_collection(best_solution_all_time)

    @staticmethod
    def to_item_collection(candidate):
        items = []
        for item in candidate.get_selected_items():
            if item[1]:
                items.append(item[0])
        return ItemCollection(items=items)

    @staticmethod
    def _select_candidate(population, total_fitness):
        """
        This method selects the best fit candidates using the Roulette Wheel Selection method.
        :param total_fitness: The total fitness of all candidates
        :return: Returns a random candidate. A candidate with better fitness scores have a better
        chance of being selected.
        """
        random_value = random.randint(0, total_fitness)
        for candidate in population:
            random_value -= candidate.get_value_of_selected()
            if random_value <= 0:
                return candidate
        return population[-1]

    @staticmethod
    def crossover(parent1, parent2, crossover_rate=0.0):
        """
        This method cross overs two parents to create a new generation.
        Randomly choose an index point and copy from 0 to index from parent one and from index to end from parent two
        This creates a new child.
        :param parent1: One of the candidates selected to be a parent.
        :param parent2: Another parent selected to be a parent.
        :param crossover_rate: The crossover rate
        :return: A tuple of child1 and child2
        """
        if random.uniform(0, 1) < crossover_rate:
            crossover = random.randint(0, len(parent1.get_selected_items()))
            selected_items1 = parent1.get_selected_items()[:crossover] + parent2.get_selected_items()[crossover:]
            selected_items2 = parent2.get_selected_items()[:crossover] + parent1.get_selected_items()[crossover:]
            return CandidateSolution(selected_items=selected_items1), CandidateSolution(selected_items=selected_items2)
        else:
            return parent1, parent2
