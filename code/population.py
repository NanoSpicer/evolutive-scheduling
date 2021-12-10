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

    def __init__(self, inputs: object, population_size: int, met: object) -> object:
        """
        Initial population operator.
        When an instance is constructed, the initial population is also created
        """
        self.method = met
        self.results = None
        self.error = err.OurError()
        self.inputs = inputs
        self.population_size = population_size  # how many genotype instances (i.e. cardinality of population)
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
        # If error in first genotype, propagate error
        if self.population[0].error.has_error():
            self.population[0].error.print()
            self.error.set_error(err.ERR_POPULATION_NOT_STABLISHED)

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
            numeros_interesantes = list(
                filter(
                    lambda el: gen.slot_value_is_assigned(el),  # el != gen.AVAILABLE and el != gen.NOT_AVAILABLE,
                    list(numeros_de_la_derecha)
                )
            )

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
            genotype.mutate()


    def fit(self, iterations: int = 10000):
        """
        Start evolutive algorithm until iterations exhaust

        :param iterations: number of iterations to execute
        :return: nothing
        """
        cpt = 0
        while cpt < iterations:
            list_of_parents = self.select_parents()
            self.crossover(list_of_parents)
            self.mutate_population()
            self.select_survivors()
            cpt += 1

        return 0.5