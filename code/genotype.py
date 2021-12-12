"""
Class Genotype:

    It codes the genotype representation and provides:
    - evaluation function (fitness function)
"""
import random
import re

import numpy as np
from utils import windowed, all_items_are_same
import our_error as err


available_char = 'a'
not_available_char = 'n'
assigned_char = 'o'

def transformar_asignacion(valor_hora):
    char_lookup = {NOT_AVAILABLE: not_available_char, AVAILABLE: available_char}
    return char_lookup.get(valor_hora, assigned_char)


UNAVAILABLE_REGEX = f"{not_available_char}+"
AVAILABLE_REGEX = f"{available_char}+"
ASSIGNED_REGEX = f"{assigned_char}+"
AVAILABLE_OR_NOT_AVAILABLE_REGEX = f"({available_char}|{not_available_char})*"
ASSIGNED_AVAILABLE_ASSIGNED_REGEX = f"{assigned_char}+{available_char}+{assigned_char}+"
INTERRUPTION_REGEX = f"^{AVAILABLE_OR_NOT_AVAILABLE_REGEX}{ASSIGNED_AVAILABLE_ASSIGNED_REGEX}{AVAILABLE_OR_NOT_AVAILABLE_REGEX}$"
IDLE_STARTING_DAYS_REGEX = f"^{UNAVAILABLE_REGEX}{AVAILABLE_REGEX}{ASSIGNED_REGEX}$"

EMPTY_SPOT_REGEX = f"{assigned_char}+{available_char}+{assigned_char}+"
# IDLE spots regex (a|n)*o+
IDLE_SPOTS_REGEX = f"^{AVAILABLE_OR_NOT_AVAILABLE_REGEX}{EMPTY_SPOT_REGEX}({EMPTY_SPOT_REGEX})*{AVAILABLE_OR_NOT_AVAILABLE_REGEX}$"


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

DIAS_LECTIVOS = list(range(5))
DIAS_SEMANA = list(range(7))

def get_daily_bounds(dia):
    inicio_dia = dia * SLOTS_PER_DAY
    final_dia = inicio_dia + SLOTS_PER_DAY
    return inicio_dia, final_dia


class NotFound(BaseException):
    pass

#
# Class Genotype()
#
class Genotype:
    # La lista de todos los profesores con sus tareas asignadas

    def __init__(self, prof_list, subject_list, assign_list, class_list, horario):
        self.score: int = 0  # my score, it's updated by the function 'evaluate'
        self.assignations_by_id = {assignment['id']: assignment for assignment in assign_list}
        self.prof_list = prof_list
        self.subject_list = subject_list
        self.assign_list = assign_list
        self.class_list = class_list
        self.horario = horario
        self.row_count = len(prof_list)
        self.col_count = 1 + DAYS_PER_WEEK * SLOTS_PER_DAY
        self.error = err.OurError()
        self.horario_full = np.full(
            (self.row_count, self.col_count),
            NOT_AVAILABLE,
            dtype=int
        )
        for (i, dia) in enumerate(horario):
            for valor in dia:
                self.horario_full[i, valor] = AVAILABLE

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

    @staticmethod
    def _class_col_index():
        # It's last column
        return DAYS_PER_WEEK * SLOTS_PER_DAY

    def _set_professors_availability(self):
        last_col_index = self._professor_col_index()
        for (i, prof) in enumerate(self.prof_list):
            prof_row = self.data_set[i]
            self._set_availability(prof_row, prof, self.horario_full)
            prof_row[last_col_index] = prof['idProfesor']

    def _find_row_index_for_professor_id(self, prof_id):
        index = 0
        prof_id_col_index = self._professor_col_index()
        for row in self.data_set:
            if row[prof_id_col_index] == prof_id:
                return index
            index += 1
        # Can't return -1 as that returns the last item in the list
        raise NotFound()

    @staticmethod
    def _find_row_index_for_class_id(schedule, class_id):
        index = 0
        class_id_col_index = Genotype._class_col_index()
        for row in schedule:
            if row[class_id_col_index] == class_id:
                return index
            index += 1
        raise NotFound()

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
                    f"Not enough available slots for assignment({assignment['id']})"
                )
                self.error.print()

    def _do_random_assignment(self, assignation, row_index):
        hours = assignation['horas']
        while hours > 0:
            random_col_index = random_slot_index()
            if self._is_available(row_index, random_col_index):
                self.data_set[row_index][random_col_index] = assignation['id']
                hours -= 1

    def _can_be_assigned(self, assignation, row_index, col_index):
        return (
            col_index != 168
            and
            self._is_available(row_index, col_index)
            and
            not self._assignation_collides(assignation, col_index)
        )

    def _is_available(self, row_index, col_index):
        return col_index != 168 and self.data_set[row_index][col_index] == AVAILABLE

    def _assignation_collides(self, assignation, col_index, skip_row_index=None):
        if col_index == 168:
            return True
        # no existe celda en columna cuya idClase sea igual al idClase de asignation
        for (row_index, row) in enumerate(self.data_set):
            if row_index == skip_row_index:
                continue
            cell_value = row[col_index]
            # cell_value can be: NOT_AVAILABLE (-1), AVAILABLE (0) or the id_assignament
            if slot_value_is_assigned(cell_value):
                cell_assignation = self.assignations_by_id[cell_value]
                if cell_assignation['idClase'] == assignation['idClase']:
                    return True

        return False

    @staticmethod
    def _count_available_slots_for_row(row: np.ndarray) -> int:
        # return (row == AVAILABLE).sum()
        return (row[:-1] == AVAILABLE).sum()  # Avoid last column

    @staticmethod
    def _set_availability(prof_row: list, profesor, horario_full):
        weekday_index = MONDAY
        # availability_for_day: [[int],...]
        for availability_for_day in profesor['disponibilidad']:
            for available_hour in availability_for_day:
                matrix_col_index = ((weekday_index * 24) + available_hour)
                if horario_full[weekday_index, available_hour] == AVAILABLE:
                    prof_row[matrix_col_index] = AVAILABLE

            weekday_index += 1

    def _soft_rule1(self, schedule) -> int:
        # 1. Penalizar los horarios de cursos con muchas horas en el mismo día (> 8 horas).
        MAX_HORAS = 8
        tiene_demasiadas_horas = 0

        for row in schedule:
            for dia in DIAS_LECTIVOS:
                initial, final = get_daily_bounds(dia)
                cpt = sum(1 for hour in range(initial, final) if slot_value_is_assigned(row[hour]))
                if cpt > MAX_HORAS:
                    tiene_demasiadas_horas += 1

        return tiene_demasiadas_horas

    def _soft_rule2(self, schedule) -> int:
        """
        2. Penalizar los horarios de profesores con muchas horas en el mismo día.
        A partir de estos datos: (https://www.ccoo.es/c8b894c3e49f175d22abe75391251c93000063.pdf)
        Curso 2018-2019: 18 horas lectivas/semana., sale que el profesor debe tener 3,6h lectivas al dia de promedio
        :return:
        """
        MAX_HORAS = 3  # 18/5 -> 3,6 trunc(3,6) -> 3
        tiene_demasiadas_horas = 0

        for row in self.data_set:
            for dia in DIAS_LECTIVOS:
                initial, final = get_daily_bounds(dia)
                cpt = sum(1 for hour in range(initial, final) if slot_value_is_assigned(row[hour]))
                if cpt > MAX_HORAS:
                    tiene_demasiadas_horas += 1

        return tiene_demasiadas_horas

    def _soft_rule3(self, schedule) -> int:
        # 3. Penalizar los horarios de cursos que tengan asignaturas con más de 2 horas de docencia de la misma asignatura por día.
        asignaturas_con_mas_de_dos_horas_de_docencia_por_dia = 0
        MAX_HORAS = 2
        for row in schedule:
            for dia in DIAS_LECTIVOS:
                initial, final = get_daily_bounds(dia)
                diccionario_asignaturaid_apariciones = {asignacion['idAsignatura']: 0 for asignacion in self.assign_list}
                horas_del_dia = row[initial:final]
                for hora in horas_del_dia:
                    if slot_value_is_assigned(hora):
                        asignacion_completa = self.assignations_by_id[hora]
                        indice = asignacion_completa['idAsignatura']
                        diccionario_asignaturaid_apariciones[indice] += 1

                dicc = diccionario_asignaturaid_apariciones
                asignaturas_con_mas_de_dos_horas_de_docencia_por_dia += sum(1 for key in dicc if dicc[key] > MAX_HORAS)


        return asignaturas_con_mas_de_dos_horas_de_docencia_por_dia

    def _soft_rule4(self, schedule) -> int:
        # 4. Penalizar los horarios de curso que tengan más de dos horas la misma asignatura (curso)
        ocurrencias = 0
        for row in schedule:
            for dia in DIAS_LECTIVOS:
                initial, final = get_daily_bounds(dia)
                horas_del_dia = row[initial:final]
                agrupaciones_de_tres = windowed(horas_del_dia, 3)
                # p -> primero; s -> segundo; t -> tercero
                ocurrencias += sum(1 for [p,s,t] in agrupaciones_de_tres if slot_value_is_assigned(p) and p == s == t)

        return ocurrencias

    def _soft_rule5(self, schedule) -> int:
        # 5. Penalizar los horarios de cursos en los que una misma asignatura se imparte de forma no consecutiva en el mismo día.
        asignaciones_asignatura_no_consecutivas = 0
        for row in schedule:
            for dia in DIAS_LECTIVOS:
                initial, final = get_daily_bounds(dia)
                horas_del_dia = row[initial:final]
                horas_que_son_asignaciones = [asignacion for asignacion in horas_del_dia if slot_value_is_assigned(asignacion)]
                dicc_asignaciones_apariciones = {hora: 0 for hora in horas_que_son_asignaciones }
                for hora in horas_del_dia:
                    if dicc_asignaciones_apariciones.get(hora) is None:
                        continue
                    dicc_asignaciones_apariciones[hora] += 1

                for hora in dicc_asignaciones_apariciones:
                    n_apariciones = dicc_asignaciones_apariciones[hora]
                    existe = len([True for window in windowed(horas_del_dia, n_apariciones) if all_items_are_same(window)]) > 0
                    if not existe:
                        asignaciones_asignatura_no_consecutivas += 1

        return asignaciones_asignatura_no_consecutivas

    def _soft_rule6(self, schedule) -> int:
        # 6. Penalizar los horarios de cursos que tengan huecos. ¡Esta condición está entre hard y soft!.
        empty_spots_regex = re.compile(IDLE_SPOTS_REGEX)
        total_empty_spots = 0
        for row in schedule:
            for dia in DIAS_LECTIVOS:
                initial, final = get_daily_bounds(dia)
                horas_del_dia = row[initial:final]
                row_as_str = ''.join(transformar_asignacion(hora) for hora in horas_del_dia)
                total_empty_spots += len(empty_spots_regex.findall(row_as_str))
        return total_empty_spots

    def _soft_rule7(self, schedule) -> int:
        # 7. Penalizar los horarios de profesores que tengan huecos.
        regexp_de_interrupciones = re.compile(INTERRUPTION_REGEX)

        total_interrupciones = 0
        for row in self.data_set:
            for dia in DIAS_LECTIVOS:
                initial, final = get_daily_bounds(dia)
                horas_del_dia = row[initial:final]
                row_as_str = ''.join(transformar_asignacion(hora) for hora in horas_del_dia)
                lista_interrupciones = regexp_de_interrupciones.findall(row_as_str)
                total_interrupciones += len(lista_interrupciones)

        return total_interrupciones

    def _soft_rule8(self, schedule) -> int:
        # 8. Penalizar los horarios de profesores con horas vacías al principio del día. Es decir promover que las horas vacías estén al final del día.
        regexp_idle_day_starts = re.compile(IDLE_STARTING_DAYS_REGEX)
        total_idle_day_starts = 0
        for row in self.data_set:
            for dia in DIAS_LECTIVOS:
                initial, final = get_daily_bounds(dia)
                horas_del_dia = row[initial:final]
                row_as_str = ''.join(transformar_asignacion(hora) for hora in horas_del_dia)
                matches = regexp_idle_day_starts.findall(row_as_str)
                if len(matches) > 0:
                    total_idle_day_starts += 1  # Aunque haya más matches, solamente hay un day_start
                else:
                    pass

        return total_idle_day_starts

    def _hard_rule1(self, schedule) -> int:
        # 1. Un profesor no puede estar en dos aulas distintas a la vez. Esta es ignorable si en nuestra representación, población, y operador de mutación lo tenemos en cuenta.
        # como se tiene en cuenta en el genotipo ->
        return 0

    def _hard_rule2(self, schedule) -> int:
        # 2. Un profesor no puede impartir la asignatura, si no está en el centro.
        # como se tiene en cuenta en el genotipo ->
        return 0

    def _hard_rule3(self, schedule) -> int:
        # 3. Dos asignaturas del mismo curso no pueden coincidir en el tiempo (solaparse).
        ocurrencias = 0
        for (row_index, row) in enumerate(self.data_set):
            for (column_index, cell) in enumerate(row):
                if column_index == 168:
                    continue
                assignation = self.assignations_by_id.get(cell)
                if slot_value_is_assigned(cell) and self._assignation_collides(assignation, column_index, skip_row_index=row_index):
                    ocurrencias += 1

        return ocurrencias

    def _get_rules_vector(self) -> list:
        hard_weight = 1000
        soft_weight = 10
        rules_duples = [
            [hard_weight, self._hard_rule1],
            [hard_weight, self._hard_rule2],
            [hard_weight, self._hard_rule3],
            [soft_weight, self._soft_rule1],
            [soft_weight, self._soft_rule2],
            [soft_weight, self._soft_rule3],
            [soft_weight, self._soft_rule4],
            [soft_weight, self._soft_rule5],
            [soft_weight, self._soft_rule6],
            [soft_weight, self._soft_rule7],
            [soft_weight, self._soft_rule8]
        ]

        return rules_duples

    def to_schedule(self):
        n_rows = len(self.class_list)
        n_cols = 1 + DAYS_PER_WEEK * SLOTS_PER_DAY
        schedule = np.full((n_rows, n_cols), NOT_AVAILABLE, dtype=int)

        for (class_index, clase) in enumerate(self.class_list):
            class_id_index = Genotype._class_col_index()
            schedule[class_index, class_id_index] = clase['idClase']

        schedule = self._set_horario_ceros(schedule)

        assignations_by_id = self.assignations_by_id
        for row in self.data_set:
            for (index_col, cell) in enumerate(row):
                if not slot_value_is_assigned(cell) or index_col == 168:
                    continue

                assignacion = assignations_by_id[cell]
                id_clase = assignacion['idClase']
                row_index = Genotype._find_row_index_for_class_id(schedule, id_clase)
                schedule[row_index, index_col] = cell

        return schedule

    def _set_horario_ceros(self, schedule: np.ndarray) -> np.ndarray:
        for dia in DIAS_SEMANA:
            schedule_dia = self.horario[dia]  # [8,9,10]
            for row in schedule:
                start, _ = get_daily_bounds(dia)
                for hora in schedule_dia:
                    row[start + hora] = AVAILABLE
        return schedule

    def evaluate(self):
        """
        Fitness function: evaluates rules and saves the score
        """
        schedule = self.to_schedule()
        new_score = 0
        for [weight, rule] in self._get_rules_vector():
            new_score += weight * rule(schedule)
        self.score = new_score

    def mutate(self, prob: float) -> bool:
        """
        Mutation operator: makes a feasible mutation
        :prob: mutaion probability
        """
        assert 0.0 <= prob <= 1.0, 'prob must be between 0 and 1'
        did_mutate = random.random() <= prob

        def get_mutable_indexes(row: np.array):
            return [i for (i, x) in enumerate(row) if slot_value_is_assigned(x)]

        if did_mutate:
            for row in self.data_set:
                mutable_indexes = get_mutable_indexes(row)
                can_mutate = len(mutable_indexes) > 0
                if not can_mutate:
                    continue
                col_index = random.choice(mutable_indexes)
                col_other_index = random.choice(mutable_indexes)
                tmp_first_col = row[col_index]
                tmp_other_col = row[col_other_index]
                row[col_other_index] = tmp_first_col
                row[col_index] = tmp_other_col




def random_slot_index():
    # gets a random slot index
    # DAYS_PER_WEEK * SLOTS_PER_DAY  -> 168
    return random.randrange(0, DAYS_PER_WEEK * SLOTS_PER_DAY)  # returns index between 0 and 167


def slot_value_is_assigned(slot_value: int) -> bool:
    # True if slot_value is a valid assignment id
    return not (slot_value == NOT_AVAILABLE or slot_value == AVAILABLE)
