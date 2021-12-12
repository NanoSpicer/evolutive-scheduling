# Programa principal
#
# Práctica de confección de horarios
#
# IC - MUSI 21 22 - UIB
#
# Alumnos:
#
# Natalia Cardona
# Miquel Àngel Roman
# Lluís Bernat

# system libraries
import json
import os

# Our own classes
#
import load_save as ls
import population as pop
import sys
import shutil
# Main program
#

def process_data_sets(in_list: list, out_list: list, num_inst_list: list, methods_list: list):
    for in_dir, out_dir in zip(in_list, out_list):
        shutil.rmtree(out_dir)
        os.mkdir(out_dir)
        print(f"Loading set: {in_dir}")
        # Load data from JSON set
        loader = ls.Loader()
        loader.load(in_dir)

        if not loader.error.has_error():
            resultados = {}
            for ins in num_inst_list:
                for met in methods_list:
                    # If JSON data set is OK, then make initial population
                    population = pop.Population(inputs=loader.data,
                                                population_size=ins,
                                                met=met,
                                                mutation_prob=0.1)

                    if not population.error.has_error():
                        hiper_parametros = population.get_hiperpar()
                        json_key = ls.format_json_key(hiper_parametros)
                        # If population is feasible, then make the timetable
                        population.fit(iterations=500)

                        # At the end of work, save the results
                        saver = ls.Saver(population.get_champion(),
                                         population.get_results(),
                                         population.get_hiperpar())
                        resultados[json_key] = saver.save_results(out_dir)
                    else:
                        population.error.print()

            with open(os.path.normpath(f"{out_dir}/horarios.json"), 'w') as json_file:
                json.dump(resultados, json_file, cls=ls.NumpyEncoder)
        else:
            loader.error.print()

    return


if __name__ == '__main__':
    args = sys.argv
    HOW_MANY_SETS = [int(sys.argv[1])] if len(args) == 2 else [1, 2]
    INPUTS_REL_PATH = '../inputs/test'
    OUTPUTS_REL_PATH = '../outputs/test'

    current_program_path = os.path.dirname(os.path.realpath(__file__))

    inputs_abs_path = os.path.normpath(current_program_path + '/' + INPUTS_REL_PATH)
    outputs_abs_path = os.path.normpath(current_program_path + '/' + OUTPUTS_REL_PATH)

    in_dir_list = [f"{inputs_abs_path}{index}" for index in HOW_MANY_SETS]
    out_dir_list = [f"{outputs_abs_path}{index}" for index in HOW_MANY_SETS]

    num_instances_list = [30, 60]  # test different population cardinalities
    op_method_list = pop.METODOS_DISPONIBLES  # test the diferents operators for mutation

    process_data_sets(in_dir_list, out_dir_list, num_instances_list, op_method_list)

    print("End of process.")
