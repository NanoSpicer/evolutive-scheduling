"""
Class Population():

    It contains a population representation and provides:
    - population operator (initial population)
    - selection operator
    - mutation operator
    - crossover operator (reproduction)
"""
import copy
import random
import numpy as np

from utils import items_as_pairs
import genotype as gen


class Population:

    def __init__(self, inputs: object, population_size: int, met: object) -> object:
        """
        Initial population operator.
        When an instance is constructed, the initial population is also created
        """
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
        self.method = met
        self.results = None
        self.error = None

    def select_parents(self):
        """
        Selection operator: selects n_sets sets of p_instances each one
        """
        population = list.copy(self.population)
        shuffled_population = random.shuffle(population)
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
            num = random.randrange(0, 7*24)
            child1 = self.make_child(parent1, parent2, num)
            child2 = self.make_child(parent2, parent1, num)
            self.population.append(child1)
            self.population.append(child2)

        self.mutate_population()

    def make_child(self, parent1: gen.Genotype, parent2: gen.Genotype, num: int) -> gen.Genotype:
        child1 = copy.deepcopy(parent1)
        data_set2 = parent2.data_set

        for (index_row, row) in enumerate(child1.data_set):
            numeros_de_la_derecha = row[num:]
            numeros_interesantes = list(
                filter(
                    lambda el: el != gen.AVAILABLE and el != gen.NOT_AVAILABLE,
                    list(numeros_de_la_derecha)
                )
            )

            row_p2 = data_set2[index_row]

            for (index_col, _) in enumerate(numeros_de_la_derecha):
                for cell in row_p2:
                    if cell in numeros_interesantes:
                        numeros_interesantes.remove(cell)
                        row[num + index_col] = cell
                        break
        return child1

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