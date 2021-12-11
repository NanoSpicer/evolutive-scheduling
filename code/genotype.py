"""
Class Genotype:

    It codes the genotype representation and provides:
    - evaluation function (fitness function)
"""

import random
import numpy as np

import our_error as err

#
# Constants
#

# Related to slots set
DAYS_PER_WEEK = 7
SLOTS_PER_DAY = 24

HOURS_IN_DAY = list(range(SLOTS_PER_DAY))

# Mark slots as ...
NOT_AVAILABLE = -1
AVAILABLE = 0

# Days of week
MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6


#
# Class Genotype()
#


class Genotype:
    # La lista de todos los profesores con sus tareas asignadas

    def __init__(self, prof_list, subject_list, assign_list):
        self.score: int = 0  # my score, it's updated by the function 'evaluate'
        self.assignations_by_id = {assignment['id']: assignment for assignment in assign_list}
        self.prof_list = prof_list
        self.subject_list = subject_list
        self.assign_list = assign_list
        self.row_count = len(prof_list)
        self.col_count = 1 + DAYS_PER_WEEK * SLOTS_PER_DAY
        self.error = err.OurError()
        self.data_set = np.full(
            (self.row_count, self.col_count),
            NOT_AVAILABLE,
            dtype=int
        )
        # Set the matrix to -1 and 0 based on the professor's availability
        self._set_professors_availability()
        # Set initial assignments (populate)
        self._set_initial_assignments()
        pass

    def _professor_col_index(self):
        # It's last column
        return self.col_count - 1

    def _set_professors_availability(self):
        i = 0
        last_col_index = self._professor_col_index()
        for prof in self.prof_list:
            prof_row = self.data_set[i]
            prof_row[last_col_index] = prof['idProfesor']
            self._set_availability(prof_row, prof)
            i += 1

    def _find_row_index_for_professor_id(self, prof_id):
        index = 0
        prof_id_col_index = self._professor_col_index()
        for row in self.data_set:
            if row[prof_id_col_index] == prof_id:
                return index
            index += 1
        return -1

    def _set_initial_assignments(self):
        for assignment in self.assign_list:
            hours = assignment['horas']
            prof_id = assignment['idProfesor']
            prof_row_index = self._find_row_index_for_professor_id(prof_id)
            row = self.data_set[prof_row_index]
            available_slots = self._count_available_slots_for_row(row)
            if hours <= available_slots:
                # can do!
                self._do_random_assignment(assignment, prof_row_index)
            else:
                self.error.set_error(
                    err.ERR_GENOTYPE_UNDER_SIZED,
                    f"Not enough available slots for assignment({assignment['id']}"
                )
                self.error.print()

    def _do_random_assignment(self, assignation, row_index):
        hours = assignation['horas']
        while hours > 0:
            random_col_index = random_slot_index()
            if self._can_be_assigned(assignation, row_index, random_col_index):
                self.data_set[row_index][random_col_index] = assignation['id']
                hours -= 1

    def _can_be_assigned(self, assignation, row_index, col_index):
        return (
            self._is_available(row_index, col_index)
            and
            not self._assignation_collides(assignation, col_index)
        )

    def _is_available(self, row_index, col_index):
        return self.data_set[row_index][col_index] == AVAILABLE

    def _assignation_collides(self, assignation, col_index):
        # no existe celda en columna cuya idClase sea igual al idClase de asignation
        for row in self.data_set:
            cell_value = row[col_index]
            # cell_value can be: NOT_AVAILABLE (-1), AVAILABLE (0) or the id_assignament
            if slot_value_is_assigned(cell_value):
                cell_assignation = self.assignations_by_id[cell_value]
                if cell_assignation['idClase'] == assignation['idClase']:
                    return True

        return False

    @staticmethod
    def _count_available_slots_for_row(row: np.ndarray) -> int:

        return (row == AVAILABLE).sum()

    @staticmethod
    def _set_availability(prof_row: list, profesor):
        weekday_index = MONDAY
        # availability_for_day: [[int],...]
        for availability_for_day in profesor['disponibilidad']:
            for available_hour in availability_for_day:
                matrix_col_index = ((weekday_index * 24) + available_hour)
                prof_row[matrix_col_index] = AVAILABLE

            weekday_index += 1

    def _soft_rule1(self) -> int:
        # 1. Penalizar los horarios de cursos con muchas horas en el mismo día (> 8 horas).

        return random.randrange(0, 40)

    def _soft_rule2(self) -> int:
        # 2. Penalizar los horarios de profesores con muchas horas en el mismo día.

        return random.randrange(0, 40)

    def _soft_rule3(self) -> int:
        # 3. Penalizar los horarios de cursos que tengan asignaturas con más de 2 horas de docencia de la misma asignatura por día.

        return random.randrange(0, 40)

    def _soft_rule4(self) -> int:
        # 4. Penalizar los horarios de curso que tengan más de dos horas la misma asignatura (curso)

        return random.randrange(0, 40)

    def _soft_rule5(self) -> int:
        # 5. Penalizar los horarios de cursos en los que una misma asignatura se imparte de forma no consecutiva en el mismo día.

        return random.randrange(0, 40)

    def _soft_rule6(self) -> int:
        # 6. Penalizar los horarios de cursos que tengan huecos. ¡Esta condición está entre hard y soft!.

        return random.randrange(0, 40)

    def _soft_rule7(self) -> int:
        # 7. Penalizar los horarios de profesores que tengan huecos.

        return random.randrange(0, 40)

    def _soft_rule8(self) -> int:
        # 8. Penalizar los horarios de profesores con horas vacías al principio del día. Es decir promover que las horas vacías estén al final del día.

        return random.randrange(0, 40)

    def _hard_rule1(self) -> int:
        #1. Un profesor no puede estar en dos aulas distintas a la vez. Esta es ignorable si en nuestra representación, población, y operador de mutación lo tenemos en cuenta.
        #2. Un profesor no puede impartir la asignatura, si no está en el centro.
        #3. Dos asignaturas del mismo curso no pueden coincidir en el tiempo (solaparse).

        return random.randrange(0, 20)

    def _get_rules_vector(self) -> list:

        rules_duples = [
            [1e6, self._hard_rule1],
            [700, self._soft_rule1],
            [600, self._soft_rule2],
            [500, self._soft_rule3],
            [400, self._soft_rule4],
            [300, self._soft_rule5],
            [200, self._soft_rule6],
            [100, self._soft_rule7],
            [50, self._soft_rule8]
        ]

        return rules_duples

    def evaluate(self):
        """
        Fitness function: evaluates rules and saves the score
        """
        new_score = 0
        for rt in self._get_rules_vector():
            new_score += rt[0] * rt[1]()
        self.score = new_score
        pass

    def mutate(self, prob: float) -> bool:
        """
        Mutation operator: makes a feasible mutation
        :prob: mutaion probability
        """
        # TODO
        pass


def random_slot_index():
    # gets a random slot index
    return random.randrange(0, DAYS_PER_WEEK * SLOTS_PER_DAY)


def slot_value_is_assigned(slot_value: int) -> bool:
    # True if slot_value is a valid assignment id
    return not (slot_value == NOT_AVAILABLE or slot_value == AVAILABLE)
