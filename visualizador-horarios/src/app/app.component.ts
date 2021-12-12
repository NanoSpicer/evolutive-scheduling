import { Component } from '@angular/core';
import { BehaviorSubject, combineLatest, Observable, ReplaySubject } from 'rxjs';
import { filter, switchMap } from 'rxjs/operators';
import { AsignacionCompleta, ClaseConHorario, HorarioCompleto } from './data-types';
import { ScheduleService, Test } from './schedule.service';
import {DataSource} from '@angular/cdk/collections';



class ClaseDataSource extends DataSource<AsignacionCompleta | null> {
  private _dataStream = new ReplaySubject<Array<AsignacionCompleta | null>>();
  constructor() {
    super();
  }

  connect(): Observable<Array<AsignacionCompleta | null>> {
    return this._dataStream;
  }

  disconnect() {}

  setData(data: ClaseConHorario) {
    this._dataStream.next(data.horario);
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
  selectedTest$ = new BehaviorSubject<Test|null>(null)
  selectedMetodo$ = new BehaviorSubject<string|null>(null)
  selectedProb$ = new BehaviorSubject<string|null>(null)
  selectedSize$ = new BehaviorSubject<string|null>(null)
  selectedClaseConHorario$ = new BehaviorSubject<ClaseConHorario|null>(null)

  columnas = ['Hora', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']

  dataSource = new ClaseDataSource();

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

  constructor(private schedule: ScheduleService) {}

  onSelectTest(test: Test) {
    this.selectedTest$.next(test)
  }
}
