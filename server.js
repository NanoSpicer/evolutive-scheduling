const fs = require('fs/promises')
const express = require('express')
const cors = require('cors')
const app = express()
app.use(cors())
app.use(express.static('.'))
const host = 'http://localhost:8080/'
async function main() {
    const directoriosTest = (await fs.readdir('outputs')).filter(it => it.startsWith('test'))
    const testsDisponibles = directoriosTest.map(it => {
        return {
            nombre: it,
            inputs: inputForTest(it),
            outputs: `${host}outputs/${it}/horarios.json`
        }
    })
    app.get('/tests', (_req, res) => res.json(testsDisponibles))
    app.get('/', (req, res) => res.json({ buenas: 'noches' }))
    app.listen(8080, () => console.log('Server is ready!'))
}

main()
    .then(console.log)
    .catch(console.error)



function inputForTest(testname) {
    return {
        asignaciones: `${host}inputs/${testname}/asignaciones.json`,
        asignaturas: `${host}inputs/${testname}/asignaturas.json`,
        clases: `${host}inputs/${testname}/clases.json`,
        horario: `${host}inputs/${testname}/horario.json`,
        profesores: `${host}inputs/${testname}/profesores.json`
    }
}