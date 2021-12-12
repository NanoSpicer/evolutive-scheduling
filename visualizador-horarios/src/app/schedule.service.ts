import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { combineLatest, EMPTY, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Asignacion, AsignacionCompleta, Asignatura, Clase, ClaseConHorario, Horario, HorarioCompleto, Profesor } from './data-types';

import { groupBy } from 'lodash-es'

const HOST = 'http://localhost:8080'

export interface Test {
  nombre: string
  inputs: {
    asignaciones: string;
    asignaturas: string;
    clases: string;
    horario: string;
    profesores: string;
  },
  outputs: string;
}

export interface Options {
  populationSizes: Array<string>
  mutationMethods: Array<string>
  mutationProb: Array<string>
}

@Injectable({providedIn: 'root'})
export class ScheduleService {

  constructor(private http: HttpClient) { }


  get<T>(url: string): Observable<Array<T>> {
    return this.http.get<Array<T>>(url)
  }

  getTests(): Observable<Array<Test>> {
    return this.http.get<Array<Test>>(`${HOST}/tests`)
  }

  getTestOptions(test: Test): Observable<Options> {
    return this.http.get(test.outputs).pipe(
      map((res: any) => this.getOptions(res))
    )
  }

  getHorarioCompleto(test: Test, size: string, method: string, prob: string): Observable<HorarioCompleto> {
    const key = `${size}-${method}-${prob}`
    const {
      asignaciones,
      asignaturas,
      clases,
      profesores
    } = test.inputs
    const todo = combineLatest([
      this.get<Asignacion>(asignaciones),
      this.get<Asignatura>(asignaturas),
      this.get<Clase>(clases),
      this.get<Profesor>(profesores),
      this.http.get<any>(test.outputs)
    ])
    return todo.pipe(
      map(valores => {
        const [
          asignaciones, asignaturas, clases,
          profesores, agregadoHorario
        ] = valores
        // T_ODO! Porque en Python Serializamos el schedule como string
        // const horario = agregadoHorario[key] as Horario
        const horario = JSON.parse(agregadoHorario[key]) as Horario
        const dictAsignaturas = groupBy(asignaturas, item => item.idAsignatura)
        const dictClases = groupBy(clases, item => item.idClase)
        const dictProfesores = groupBy(profesores, item => item.idProfesor)
        const asignacionesCompletas: Array<AsignacionCompleta> = asignaciones.map(ass => {
          const profesor = dictProfesores[ass.idProfesor][0]
          const asignatura = dictAsignaturas[ass.idAsignatura][0]
          const clase = dictClases[ass.idClase][0]
          return { id: ass.id, profesor, asignatura, clase }
        })
        const dictAsignaciones = groupBy(asignacionesCompletas, ass => ass.id)
        console.log(dictAsignaciones);

        // horario = array[6] de arrays[169]
        const horarios: Array<ClaseConHorario> = horario.map(horarioClase => {
          const isLast = (i: number) => i === 168
          const mapToAsignacion = (val: number) => {
            const invalidos = [-1,0]
            return invalidos.includes(val) ? null : dictAsignaciones[val][0]
          }
          const idClase = horarioClase[168]
          console.log(idClase, dictClases[idClase]);
          // const idClase = horarioClase[168]

          const asignacionesCompletas: Array<AsignacionCompleta | null> =
            horarioClase
              .map((val, i) => isLast(i) ? undefined : mapToAsignacion(val))
              .filter(it => it !== undefined) as Array<AsignacionCompleta | null>;
          return {
            clase: dictClases[idClase][0],
            horario: asignacionesCompletas
          }
        })

        return { clasesConHorario: horarios }
      }),
    )

  }

  private getOptions(res: any): Options {
    const mutationMethods = new Set<string>()
    const populationSizes = new Set<string>()
    const mutationProb = new Set<string>()

    Object
      .keys(res)
      .map(key => key.split('-'))
      .forEach(([populationSize, method, prob]) => {
        populationSizes.add(populationSize)
        mutationMethods.add(method)
        mutationProb.add(prob)
      })

    return {
      mutationMethods: Array.from(mutationMethods),
      populationSizes: Array.from(populationSizes),
      mutationProb: Array.from(mutationProb)
    }
  }


}
