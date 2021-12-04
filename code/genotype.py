"""
Class Genotype:

    It codes the genotype representation and provides:
    - evaluation function (fitness function)
"""

import numpy as np

class Genotype:

    def __init__(self, data_set):

        self.data_set = data_set

    def evaluate(self) -> float:
        """
        Fitness function: evaluates hard and soft rules and calculates the score

        Returns: float with score
        """
        pass

    def mute(self) -> bool:
        """
        Mutation operator: makes a feasible mutation

        Returns True or False accordingly
        """
        pass