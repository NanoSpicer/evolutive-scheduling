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
def process_data_sets(ds_list: list, instances_list: list):

	for data_set_files in ds_list:

		## Load data from JSON set
		loader = ls.Loader()
		loader.load(data_set_files)

		if loader.error == None:

			for ins in instances_list:
				## If JSON data set is OK, then make initial population
				population = pop.Population(loader.data, instances=ins)
				population.populate()

				if population.error == None:

					## If population is feasible, then make the timetable
					population.fit()

					## At the end of work, save the results
					saver = ls.Saver(population.results)
					saver.save_results(data_set_files)

	return


if __name__ == '__main__':

	data_set_list = [
		'../data/set_1',
#        '../data/set_2'
		]

	instances_list = [10, 50]

	process_data_sets(data_set_list, instances_list)

