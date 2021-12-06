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
        archivos = [
            "asignaciones",
            "asignaturas",
            "clases",
            "horario",
            "profesores"
        ]

        complete_relative_paths = list(
            map(lambda nombre_archivo: f"{in_files_dir}/{nombre_archivo}.json", archivos)
        )
        self.data = {}
        index = 0
        for dir in complete_relative_paths:
            with open(dir) as file:
                values = json.load(file)
                key = archivos[index]
                self.data[key] = values
            index += 1

        return self.data


"""
Class Saver:
    It serializes and saves results to JSON files
"""

class Saver:
    def __init__(self, results: object):
        pass

    def save_results(self, out_files_dir):
        pass
