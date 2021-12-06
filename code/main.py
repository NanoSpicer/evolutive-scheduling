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

# Our own classes
#
import load_save as ls
import population as pop


# Main program
#
def process_data_sets(in_list: list, out_list: list, num_inst_list: list, methods_list: list):
    for in_dir, out_dir in zip(in_list, out_list):

        # Load data from JSON set
        loader = ls.Loader()
        loader.load(in_dir)

        if loader.error is None:

            for ins in num_inst_list:
                for met in methods_list:
                    # If JSON data set is OK, then make initial population
                    population = pop.Population(inputs=loader.data,
                                                n_ins=ins,
                                                met=met)
                    population.populate()

                    if population.error is None:
                        # If population is feasible, then make the timetable
                        population.fit()

                        # At the end of work, save the results
                        saver = ls.Saver(population.results)
                        saver.save_results(out_dir)

    return


if __name__ == '__main__':
    how_many_sets = 2

    in_dir_list = list(map(lambda index: f"../inputs/test{index}", range(1, how_many_sets + 1)))
    out_dir_list = list(map(lambda index: f"../outputs/test{index}", range(1, how_many_sets + 1)))
    num_instances_list = [10, 50] # test different population cardinalities
    op_method_list = ['mute1', 'mute2']  # test the diferents operators for mutation

    process_data_sets(in_dir_list, out_dir_list, num_instances_list, op_method_list)

    print("End of process.")
