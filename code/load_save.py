import json
import matplotlib.pyplot as plt
import datetime
import numpy as np
import os

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




class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)



"""
Class Saver:
    It serializes and saves results to JSON files
"""

#
# Constants
#

PLOT_SUFFIX_NAME = "_plot_fitness"
PLOT_EXT_NAME = ".png"


class Saver:
    def __init__(self, best_genotype: gen.Genotype,
                 results: list, hiperpar: dict):
        self.best_genotype = best_genotype
        self.results = results
        self.hiperpar = hiperpar
        self.hiperpar_str = dict2str(hiperpar)
        pass

    def save_results(self, out_files_dir: str) -> str:
        now = datetime.datetime.now()
        date_mark = now.strftime("%Y%m%d_%H%H")
        instance_out_dir = os.path.normpath(f"{out_files_dir}/{date_mark}{self.hiperpar_str}")
        # print last 10 results
        # print(self.results[-10:])
        # save results list as plot
        plot_file_name = f"{instance_out_dir}{PLOT_SUFFIX_NAME}{PLOT_EXT_NAME}"
        print(f"Saving fitness function plot to {plot_file_name}")
        self._save_plot_results(plot_file_name)
        best_schedule = self.best_genotype.to_schedule()
        return best_schedule

    def _save_plot_results(self, file_name: str):
        """
        Create and save fitness plot to file_name
        :param file_name:
        """
        # creating plotting data
        xaxis = range(len(self.results))
        yaxis = self.results

        # plotting
        plt.figure(1)
        plt.plot(xaxis, yaxis)
        plt.xlabel("Iterations")
        plt.ylabel("Fitness score")
        plt.title("Fitness function evolution")

        # saving the file
        plt.savefig(file_name)
        plt.close()
        pass

def dict2str(d: dict) -> str:
    serial = ''
    for key in d:
        serial += f"_{key}_{d[key]}"
    return serial


def format_json_key(d: dict) -> str:
    separador = '-'
    population_size = d['ps']
    metodo = d['met']
    prob_mutacion = d['mp']
    return f"{population_size}{separador}{metodo}{separador}{prob_mutacion}"

