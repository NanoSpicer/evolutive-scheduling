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

> Poner enunciado resumido

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

## Implementación

### Entrada de datos

> Poner estructuras JSON que diseñó MA ...

### Genotipo

Nuestro genotipo será una estructura que puede 
concebirse como una tabla de dos dimensiones, donde:

- Las filas representan la *lista de tareas* de cada profesor. 
Es decir, existe una fila para cada profesor. 

- Las columnas representan cada una un *slot* horario. 
Todas las celdas de la misma columna representan el mismo *slot* temporal. 

La implementación de este genotipo la haremos 
usando un dicconario de *Python* cuya clave será 
el identificador del profesor y su contenido
una lista de enteros. 
Por tanto el diccionario poseerá P entradas 
y por tanto P listas, 
cada una con 168 posiciones (7 x 24), 
siendo P el cardinal del conjunto de profesores.
El primer *slot* de la lista se corrsponde 
con la franja horaria 00:00 a 01:00 del lunes 
y el último con 
la franja horaria 23:00 a 24:00 del domingo.

Podemos pensar en esta estructura como una matriz 
de este estilo:

| Id profesor | 0 | 1 | ... | 8 | 9 | 10 | 11 | ... | 167 |
| :---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ND | ND | ... | ND | 2 | 5 | 3 | ... | ND |
| 2 | ND | ND | ... | ND | 6 | Libre | 4 | ... | ND |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ND |
| 25 | ND | ND | ... | ND | ND | 7 | Libre | --- | ND |

En el ejemplo anterior:
- el profesor con identificador 1 tiene asignada:
    - la tarea 2 el lunes a las 9
    - la tarea 5 el lunes a las 10
    - la tarea 3 el lunes a las 11
- el profesor con identificador 2 tiene asignada: 
    - la tarea 6 el lunes a las 9
    - un *slot* libre el lunes a las 10
    - la tarea 4 el lunes a la 11
- el profesor con identificador 25 tiene asignada:
    - la tarea 7 el lunes a las 10
    - un *slot* libre el lunes a las 11

Los *slots* en los que el profesor no està disponible, 
están marcados con un valor especial que llamaremos *ND*.
Los *slots* en los que el profesor sí está disponible, 
pero no tienen ninguna tarea, se marcan con otro valor 
especial al que llamaremos *Libre*.

### Definición de tarea

Cada tarea es un tupla 
que consta de los siguientes elementos: 

- idTarea: entero que actua de clave única 
para esta tupla. 
Este valor se le asigna en el momento de su creación
en memoria de forma secuencial empezando por 1.
- idClase: entero que identifica 
de forma unívoca una clase de todas las definidas.
- horas: cantidad de *slots*  que esta tarea debe
de forma obligatoria asignarse.
- idAsignatura: entero que identifica la asignatura.
- idProfesor: entero del identificador del profesor.
- vida: contador del número de asignaciones disponibles.
Inicialmente tiene el mismo valor que `horas` y sa va decrementado una unidad por asignación. 

