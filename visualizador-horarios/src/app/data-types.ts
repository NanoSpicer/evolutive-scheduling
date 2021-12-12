

export interface Asignacion {
  id: number
  idClase: number
  idProfesor: number
  idAsignatura: number
  horas: number
}

export interface AsignacionCompleta {
  id: number
  clase: Clase
  profesor: Profesor
  asignatura: Asignatura
}

export interface Asignatura {
  idAsignatura: number
  nombre: string
}
export interface Clase {
  idClase: number
  nombre: string
  totalHorasSemanales: number
}

export interface Profesor {
  idProfesor: number,
  nombre: string
  disponibilidad: Array<Array<number>>
}

export type Horario = Array<Array<number>>


export interface ClaseConHorario {
  clase: Clase
  horario: Array<AsignacionCompleta | null>
}

export interface HorarioCompleto {
  clasesConHorario: Array<ClaseConHorario>
}
