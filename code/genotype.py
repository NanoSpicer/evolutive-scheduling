"""
Class Genotype:

    It codes the genotype representation and provides:
    - evaluation function (fitness function)
"""

import random
import numpy as np

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
        self.assignations_by_id = {assignment['id']: assignment for assignment in assign_list}
        self.prof_list = prof_list
        self.subject_list = subject_list
        self.assign_list = assign_list
        self.row_count = len(prof_list)
        self.col_count = 1 + DAYS_PER_WEEK * SLOTS_PER_DAY
        self.error = None
        self.data_set = np.full(
            (self.row_count, self.col_count),
            NOT_AVAILABLE,
            dtype=int
        )
        # Set the matrix to -1 and 0 based on the professor's availability
        self._set_professors_availability()
        # Set initial assignments (populate)
        self._set_initial_assignments()

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
                self.error = f"Not enough available slots for assignment({assignment['id']})"

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

    def evaluate(self) -> float:
        """
        Fitness function: evaluates hard and soft rules and calculates the score

        Returns: float with score
        """
        pass

    def mutate(self) -> bool:
        """
        Mutation operator: makes a feasible mutation

        Returns True or False accordingly
        """
        pass


def random_slot_index():
    # gets a random slot index
    return random.randrange(0, DAYS_PER_WEEK * SLOTS_PER_DAY)


def slot_value_is_assigned(slot_value: int) -> bool:
    # True if slot_value is a valid assignment id
    return not (slot_value == NOT_AVAILABLE or slot_value == AVAILABLE)
