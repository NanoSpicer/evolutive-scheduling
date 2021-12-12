import { Component } from '@angular/core';
import { BehaviorSubject, combineLatest, Observable, ReplaySubject } from 'rxjs';
import { filter, map, switchMap } from 'rxjs/operators';
import { AsignacionCompleta, ClaseConHorario, HorarioCompleto } from './data-types';
import { ScheduleService, Test } from './schedule.service';
import { DataSource } from '@angular/cdk/collections';


export interface Fila {
  hora: string;
  lunes: string | null
  martes: string | null
  miercoles: string | null
  jueves: string | null
  viernes: string | null
}


export function windowed<T>(items: Array<T>, windowSize: number): Array<Array<T>> {
  const nItems = items.length
  let start = 0
  let finalIndex = start + windowSize
  const result: Array<Array<T>> = []

  while (finalIndex <= nItems) {
    const sublista = items.slice(start, finalIndex)
    result.push(sublista)
    start++
    finalIndex = start + windowSize
  }
  return result
}


function asignacionOrNullToString(
  asignacion: AsignacionCompleta | null,
  index: number
) {
  switch(true) {
    case asignacion != null: return asignacion?.asignatura.nombre!
    case asignacion == null && index < 9: return ''
    case asignacion == null && index > 16: return ''
    case asignacion == null && index === 11: return 'Recreo'
    case asignacion == null && index === 15: return 'Comida'
    default: return ''
  }
}

class ClaseDataSource extends DataSource<Fila> {
  private _dataStream = new ReplaySubject<Array<Fila>>();

  private dictHoras: {
    [key: number]: string
  }

  constructor(source$: Observable<ClaseConHorario>) {
    super();
    const kvPairs = Array.from({ length: 24 }).map((_, i) => {
      const str = i < 10 ? `0${i}:00` : `${i}:00`
      return [i, str]
    })
    this.dictHoras = [{}, ...kvPairs].reduce((acc, current) => {
      const [key, val] = current as [number, string]
      const newDict: any = {}
      newDict[key] = val
      const res = { ...acc, ...newDict }
      return res
    })

    source$.subscribe(d => this.setData(d))
  }

  connect(): Observable<Array<Fila>> {
    return this._dataStream.asObservable();
  }

  disconnect() { }

  private getVentanasDeSemana<T>(items: Array<Array<T>>): [Array<T>,Array<T>,Array<T>,Array<T>,Array<T>] {
    const offset = 24
    return [
      items[0 * offset],
      items[1 * offset],
      items[2 * offset],
      items[3 * offset],
      items[4 * offset]
    ]
  }

  setData(data: ClaseConHorario) {
    const horario = data.horario;
    const ventanasDe24 = windowed(horario, 24)
    const [lunes, martes, miercoles, jueves, viernes] = this.getVentanasDeSemana(ventanasDe24)
    console.log('DEBUG', lunes);

    const filas = Array.from({length: 24}).map((_, index) => {
      const hora = this.dictHoras[index]
      const [lunesTs, martesTs, miercolesTs, juevesTs, viernesTs] = (
        [lunes[index], martes[index], miercoles[index], jueves[index], viernes[index]]
      )

      return {
        hora,
        lunes: asignacionOrNullToString(lunesTs, index),
        martes: asignacionOrNullToString(martesTs, index),
        miercoles: asignacionOrNullToString(miercolesTs, index),
        jueves: asignacionOrNullToString(juevesTs, index),
        viernes: asignacionOrNullToString(viernesTs, index)
      }
    })
    this._dataStream.next(filas);
  }
}




@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'visualizador-horarios';
  tests$: Observable<Array<Test>> = this.schedule.getTests()
  selectedTest$ = new BehaviorSubject<Test | null>(null)
  selectedMetodo$ = new BehaviorSubject<string | null>(null)
  selectedProb$ = new BehaviorSubject<string | null>(null)
  selectedSize$ = new BehaviorSubject<string | null>(null)
  selectedClaseConHorario$ = new BehaviorSubject<ClaseConHorario | null>(null)

  columnas = ['Hora', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']

  dataSource = new ClaseDataSource(
    this.selectedClaseConHorario$.pipe(
      filter(it => it != null),
      map(val => val as ClaseConHorario)
    )
  );

  options$ = this.selectedTest$.pipe(
    filter(val => val != null),
    switchMap(val => this.schedule.getTestOptions(val!))
  )
  horario$: Observable<HorarioCompleto> =
    combineLatest([this.selectedTest$, this.selectedMetodo$, this.selectedProb$, this.selectedSize$])
      .pipe(
        filter(arrayValores => arrayValores.every(entry => entry != null)),
        switchMap(arrayValores => {
          const [selectedTest, selectedMetodo, selectedProb, selectedSize] = arrayValores
          return this.schedule.getHorarioCompleto(selectedTest!, selectedSize!, selectedMetodo!, selectedProb!)
        })
      )

  constructor(private schedule: ScheduleService) { }

  onSelectTest(test: Test) {
    this.selectedTest$.next(test)
  }
}
