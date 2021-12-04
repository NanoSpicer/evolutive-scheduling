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

    def __init__(self, inputs: object, n_ins: int, met: object) -> object:

        self.inputs = inputs
        self.n_ins = n_ins  # how many genotype instances (i.e. cardinality of population)
        self.method = met
        self.results = None
        self.error = None

    def populate(self):
        """
        Initial population operator
        """
        pass

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