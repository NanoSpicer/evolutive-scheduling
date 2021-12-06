"""
Class Population():

    It contains a population representation and provides:
    - population operator (initial population)
    - selection operator
    - mutation operator
    - crossover operator (reproduction)
"""

import numpy as np

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

    def select(self, n_sets: int, p_instances: int):
        """
        Selection operator: selects n_sets sets of p_instances each one
        """
        pass

    def crossover(self):
        """
        Crossover operator: creates a new set of genotype instances
        using the parents information

        :return:
        """
        pass

    def fit(self, iterations: int = 10000):
        """
        Start evolutive algorithm until iterations exhaust

        :param iterations: number of iterations to execute
        :return: nothing
        """

        pass