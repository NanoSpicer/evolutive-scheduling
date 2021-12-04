# Generación de horarios

## Identificación

Assignatura: 11753 Inteligencia Computacional

Estudios: MUSI - UIB - Curso 21/22

Profesor: Dr. Sebastián Massanet Massanet
(s.massanet@uib.es)

Alumnos: 
- Natalia Erika Cardona Matamoros
(erika-natalia.cardona1@estudiant.uib.cat)
- Miquel Àngel Roman Colom 
(miquel-angel.roman1@estudiant.uib.cat)
- Lluís Bernat Ladaria 
(lluis.bernat2@estudiant.uib.cat)

## Enunciado 

El objetivo de esta entrega 
es implementar un algoritmo evolutivo 
para la elaboración de horarios 
en un centro educativo. 
El algoritmo tendrá como entrada la siguiente
información:

- Un número de clases (grupos de alumnos). 
Ningún alumno está en dos clases.
- Para cada clase, 
un número total de horas semanales 
y una lista de asignaturas.
Cada asignatura tendrá un número 
de horas semanales establecido y un profesor asignado. 
*Tened en cuenta que un profesor puede dar asignaturas en varias
clases distintas y varias asignaturas a la misma clase*.
- Para cada profesor se dispondrá de su disponibilidad horaria, 
puede ser que no esté disponible en determinadas horas de la semana.
- Las franjas horarias semanales disponibles para impartir las clases.

La salida del algoritmo será el horario semanal de cada clase. Supondremos que el centro establece una aula fija 
para cada clase de manera que el algoritmo no tiene que asignar aulas.
1. Estableced cuáles son las restricciones *soft* y *hard* de vuestro algoritmo y justificadlas.
1. Explicad claramente cuál es la codificación usada, cuáles son los parámetros del algoritmo y su función de *fitness*. 
Justificad su elección.
1. Cread varias entradas con distintos grados de dificultad 
y analizad los resultados obtenidos. 
Podéis utilizar como entrada listas de asignaturas y sus horas
semanales de distintos cursos de secundaria y bachillerato.
1. Proponed alguna modificación al algoritmo 
y analizad los resultados obtenidos.
Esta modificación puede ser un nuevo operador de mutación 
o recombinación, 
una nueva estrategia de selección de los individuos de la nueva generación, etc.

Podéis implementar los algoritmos 
en el lenguaje que consideréis más adecuado. 
Los algoritmos tienen que ir acompañados de:
1. Todos los ficheros fuente.
1. En la memoria se tiene que explicar brevemente 
cada función implementada.


## Introducción

En este trabajo vamos a desarrollar un algoritmo evolutivo 
en lenguaje *Python* 
para la confección de horarios siguiendo 
las pautas del [enunciado](#Enunciado). 
Para dar cuenta de ello se divide este trabajo 
en los siguientes apartados:
- [Restricciones](#Restricciones): se detallan 
el conjunto de restricciones fuertes 
(i.e. las que una solución válida debe cumplir) 
y el conjunto de restricciones débiles 
(i.e. todas las que una solución debe intentar cumplir).
- [Implementación](#Implementación): en este 
apartado se presenta el formato 
de las entradas al proceso, 
el genotipo, la representación interna de ambos, 
el método de población inicial, 
la función de *fitness*, 
y los diferentes operadores 
(mutación, recombinación y selección).
- [Pruebas y análisis](#Pruebas-y-análisis): donde 
se analizan los resultados obtenidos para diferentes 
ejemplos que se suministran.
- [Cambios y resultados](#Cambios-y-resultados): en 
este apartado se propone un cambio y se presentan
las variaciones obtenidas en el desempeño de los ejemplos.
- [Conclusiones](#Conclusiones): finalmente
un último apartado de conclusiones finaliza este trabajo.


## Restricciones

Consideraremos dos conjuntos de restricciones. 

### Conjunto de restricciones *hard*

Consideramos tres restricciones fuertes:

1. Un profesor no puede estar en dos aulas distintas a la vez. Esta es ignorable si en nuestra representación, población, y operador de mutación lo tenemos en cuenta.

1. Un profesor no puede impartir la asignatura, si no está en el centro.

1. Dos asignaturas del mismo curso no pueden coincidir en el tiempo (solaparse).


### Conjunto de restricciones *soft*

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
Los *slots* tienen una duración de 60 minutos.

La implementación de este genotipo la haremos 
usando un diccionario (de *Python*) cuya clave será 
el identificador del profesor y su contenido
una lista de enteros. 
Por tanto el diccionario poseerá P entradas 
y por tanto P listas, 
cada una con 168 posiciones (7 x 24), 
siendo P el cardinal del conjunto de profesores.
El primer *slot* de la lista se corresponde 
con la franja horaria 00:00 a 01:00 del lunes 
y el último con 
la franja horaria 23:00 a 24:00 del domingo.

Podemos pensar en esta estructura como una matriz 
de este estilo:

| IdProfesor | 0 | 1 | ... | 8 | 9 | 10 | 11 | ... | 167 |
| :---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ND | ND | ... | ND | 2 | 5 | 3 | ... | ND |
| 2 | ND | ND | ... | ND | 6 | Libre | 4 | ... | ND |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ND |
| 25 | ND | ND | ... | ND | ND | 7 | Libre | --- | ND |

En el ejemplo anterior:
- el profesor con `idProfesor` 1 tiene asignada:
    - la tarea con `idTarea` 2 el lunes a las 9
    - la tarea con `idTarea` 5 el lunes a las 10
    - la tarea con `idTarea` 3 el lunes a las 11
- el profesor con `idProfesor` 2 tiene asignada: 
    - la tarea con `idTarea` 6 el lunes a las 9
    - un *slot* libre el lunes a las 10
    - la tarea con `idTarea` 4 el lunes a la 11
- el profesor con `idProfesor` 25 tiene asignada:
    - la tarea con `idTarea` 7 el lunes a las 10
    - un *slot* libre el lunes a las 11

Los *slots* en los que el profesor no està disponible, 
están marcados con un valor especial que llamaremos *ND*.
Los *slots* en los que el profesor sí está disponible, 
pero no tienen ninguna tarea, se marcan con otro valor 
especial al que llamaremos *Libre*.

### Definición de tarea

Cada tarea es un tupla 
que consta de los siguientes campos: 

- `idTarea`: entero que actua de clave única 
para esta tupla. 
Este valor se le asigna en el momento de su creación
en memoria de forma secuencial empezando por el número 1.
- `idClase`: entero que identifica 
de forma unívoca una clase de entre todas las definidas.
- `horas`: cantidad de *slots* temporales que, 
de forma obligatoria,
deben asignarse a esta tarea.
- `idAsignatura`: entero que identifica 
de forma unívoca la asignatura.
- `idProfesor`: entero que identifica de forma unívoca al profesor.
- `vidas`: contador del número de asignaciones disponibles.
Inicialmente (al cargar los datos) se le asigna el mismo valor que `horas` y es decrementado una unidad por cada asignación que se le aplica. 

### Población inicial 

> Algoritmo de población inicial

### Función de *fitness*

> Pesos de la función

### Operador de selección

> Cómo elegimos padres y/o supervivientes

### Operador de mutación 

> Permutación de dos tareas 
o una tarea y un *slot* libre, 
del mismo profesor (i.e. la misma fila).

### Operador de recombinación

> Elegir padres, liberar un % de tareas


## Pruebas y análisis

> Qué ejemplos hemos probado (posibles e imposibles de resolver)
y resultados de convergencia y tiempo.


## Cambios y resultados

> Cambios que hemos implementado y sus resultados.


## Conclusiones

> Ánimo que ya terminamos.