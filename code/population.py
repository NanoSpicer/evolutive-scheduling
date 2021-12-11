"""
Class Population():

    It contains a population representation and provides:
    - population operator (initial population done at init)
    - selection operator
    - mutation operator
    - crossover operator (reproduction)
"""
import copy
import random
import numpy as np

import our_error as err

from utils import items_as_pairs
import genotype as gen


class Population:

    def __init__(self, inputs: object, population_size: int, met: object, mutation_prob: float) -> object:
        """
        Initial population operator.
        When an instance is constructed, the initial population is also created
        """
        self.inputs = inputs
        self.population_size = population_size  # how many genotype instances (i.e. cardinality of population)
        self.method = met  # which method will use in some operators
        self.mutation_prob = mutation_prob
        self.best_score: int = -1  # the best score, it's updated by 'evaluate' function
        self.champion_index: int = -1  # the pos of the best genotype in population list, updated by 'evaluate' func
        self.results = []  # historical list of best scores
        self.error = err.OurError()  # instance our error object
        self.population = list(
            map(
                lambda _: gen.Genotype(
                    inputs['profesores'],
                    inputs['asignaturas'],
                    inputs['asignaciones']
                ),
                range(population_size)
            )
        )
        # If error in any genotype instance, then propagate error
        it = 0
        while it < len(self.population) and not self.population[it].error.has_error():
            if self.population[it].error.has_error():
                self.population[it].error.print()
                self.error.set_error(err.ERR_POPULATION_NOT_STABLISHED)
            it += 1

        if not self.error.has_error():
            self.evaluate_population()
            self.update_best_score()
        pass

    def get_hiperpar(self) -> dict:
        # Return hiperparameters dict
        # ps: population_size
        # met: selected method to test
        # mp: mutation probability
        hiper = {'ps': self.population_size,
                 'met': self.method,
                 'mp': self.mutation_prob}
        return hiper

    def get_champion(self) -> gen.Genotype:
        # Returns the best one
        return self.population[self.champion_index]

    def get_results(self):
        # Returns the historical score list
        return self.results

    def select_parents(self):
        """
        Selection operator: selects the parents couples

        Method: random shuffle
        """
        population = list.copy(self.population)
        shuffled_population = random.sample(population, len(population))
        return items_as_pairs(shuffled_population)

    def select_survivors(self):
        return []  # todo

    def crossover(self, list_of_parents):
        # list_of_parents: [(p1, p2), (p3, p4)]
        """
        Crossover operator: creates a new set of genotype instances
        using the parents information

        :return:
        """
        for (parent1, parent2) in list_of_parents:
            # parent1: genotype
            num = gen.random_slot_index()
            child1 = self.make_child(parent1, parent2, num)
            child2 = self.make_child(parent2, parent1, num)
            self.population.append(child1)
            self.population.append(child2)

        self.mutate_population()

    def make_child(self, parent1: gen.Genotype, parent2: gen.Genotype, partition: int) -> gen.Genotype:
        new_child = copy.deepcopy(parent1)
        data_set2 = parent2.data_set

        for (index_row, row) in enumerate(new_child.data_set):
            numeros_de_la_derecha = row[partition:]
            # slot_value_is_assigned --> el != gen.AVAILABLE and el != gen.NOT_AVAILABLE,
            numeros_interesantes = [el for el in numeros_de_la_derecha if gen.slot_value_is_assigned(el)]

            row_p2 = data_set2[index_row]
            for (index_col, _) in enumerate(numeros_de_la_derecha):
                for cell in row_p2:
                    if cell in numeros_interesantes:
                        numeros_interesantes.remove(cell)
                        row[partition + index_col] = cell
                        break
        return new_child

    def mutate_population(self):
        for genotype in self.population:
            genotype.mutate(prob=self.mutation_prob)

    def evaluate_population(self):
        for genotype in self.population:
            genotype.evaluate()
        pass

    def update_best_score(self):
        new_best_score = -1
        new_champion_index = -1
        for index, genotype in enumerate(self.population):
            if (genotype.score < new_best_score) or (new_best_score == -1):
                new_best_score = genotype.score
                new_champion_index = index
        self.champion_index = new_champion_index
        self.best_score = new_best_score
        self.results.append(new_best_score)
        pass

    def fit(self, iterations: int = 100):
        """
        Start evolutive algorithm until iterations exhaust

        :param iterations: number of iterations to execute
        :return: nothing
        """
        for it in range(iterations):
            list_of_parents = self.select_parents()
            self.crossover(list_of_parents)
            self.mutate_population()
            self.evaluate_population()
            self.select_survivors()
            self.update_best_score()

            # Print some feedback progress every 100 iterations ...
            if it % 100 == 0:
                print(f"Iteration {it + 1} form {iterations}. Fitness value: {self.best_score}")

        return 0.5
