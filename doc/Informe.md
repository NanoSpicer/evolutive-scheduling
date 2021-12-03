# Generación de horarios

## Identificación

Assignatura: Inteligencia Computacional
Estudios: MUSI - UIB

Profesor: Sebastián Massanet

Alumnos: 
- Natalia (@estudiant.uib.cat)
- Miquel Àngel Roman (@estudiant.uib.cat)
- Lluís Bernat Ladaria (lluis.bernat2@estudiant.uib.cat)

## Introducción 

> Enunciado resumido

## Implementación

### Restricciones

#### Conjunto de restricciones *hard*

Consideramos tres restricciones fuertes:

1. Un profesor no puede estar en dos aulas distintas a la vez. Esta es ignorable si en nuestra representación, población, y operador de mutación lo tenemos en cuenta.

1. Un profesor no puede impartir la asignatura, si no está en el centro.

1. Dos asignaturas del mismo curso no pueden coincidir en el tiempo (solaparse).


#### Conjunto de restricciones *soft*

El conjunto de restricciones débiles es:

1. Penalizar los horarios de cursos con muchas horas en el mismo día (> 8 horas).

2. Penalizar los horarios de profesores con muchas horas en el mismo día.

3. Penalizar los horarios de cursos que tengan asignaturas con más de 2 horas de docencia de la misma asignatura por día.

4. Penalizar los horarios de curso que tengan mas de dos horas la misma asignatura (curso)

5. Penalizar los horarios de cursos en los que una misma asignatura se imparte de forma no consecutiva en el mismo día.

6. Penalizar los horarios de cursos que tengan huecos. ¡Esta condición está entre hard y soft!.

7. Penalizar los horarios de profesores que tengan huecos.

8. Penalizar los horarios de profesores con horas vacías al principio del día. Es decir promover que las horas vacías estén al final del día.

### Entrada de datos

Poner estructuras JSON...

### Genotipo

Nuestro genotipo es una matriz con la siguiente estructura: 

- Filas: representan la *lista de tareas* de cada profesor. 
Es decir, existe una fila para cada profesor. 

- Columnas: cada columna representa un *slot* horario. 
Todas las celdas de la misma columna representan el mismo *slot*. 

Así nuestro genotipo será un dicconario de listas de enteros 
con P entradas y valores por lista, 
siendo P el cardinal del conjunto de profesores.

Podemos pensar en esta estructura como una matriz 
de este estilo:

| Id profesor | 0 | 1 | ... | 8 | 9 | 10 | 11 | ... | 167 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ND | ND | ... | ND | 2 | 5 | 3 | ... | ND |
| 2 | ND | ND | ... | ND | 6 | Libre | 4 | ... | ND |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ND |
| 5 | ND | ND | ... | ND | ND | 7 | Libre | --- | ND |

En el ejemplo anterior:
- el profesor 1 tiene asignada:
    - la tarea 2 el lunes a las 9
    - la tarea 5 el lunes a las 10
    - la tarea 3 el lunes a las 11
- el profesor 2 tiene asignada: 
    - la tarea 6 el lunes a las 9
    - un *slot* libre el lunes a las 10
    - la tarea 4 el lunes a la 11
- el profesor 5 tiene asignada:
    - la tarea 7 el lunes a las 10
    - un *slot* libre el lunes a las 11

Los *slots* en los que el profesor no està disponible, 
están marcados con un valor especial que llamaremos *ND*.

