import numpy as np
import json


"""
Class Loader: 
    It loads data from JSON files to memory structures
"""

class Loader:
    def __init__(self):
        self.data = None
        self.error = None

    def load(self, in_files_dir):
        pass


"""
Class Saver:
    It serializes and saves results to JSON files
"""

class Saver:
    def __init__(self, results: object):
        pass

    def save_results(self, out_files_dir):
        pass
