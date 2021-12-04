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

    def __init__(self, data: object, instances: int) -> object:

        self.data = data
        self.instances = instances
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
        """
        pass

    def fit(self):
        pass