import json


"""
Class Loader: 
    It loads data from JSON files to memory structures
"""

import genotype as gen
import our_error as err

class Loader:
    def __init__(self):
        self.data = None
        # TODO: Add input sanitization
        self.error = err.OurError()

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
            with open(dir, encoding='utf_8') as file:
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
    def __init__(self, best_genotype: gen.Genotype,
                 results: list, hiperpar: dict):
        self.best_genotype = best_genotype
        self.results = results
        self.hiperpar = hiperpar
        pass

    def save_results(self, out_files_dir):
        # TODO save genotype and results as JSON

        # print last 10 results
        print(self.results[-10:])
        pass
