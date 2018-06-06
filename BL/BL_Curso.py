from DC import DC_Sinonimo, DC_Curso


def getCursoDescripcion(connection, data):
    if data[0] == ' ':
        data = data[1:len(data)]
    if data[len(data)-1] == ' ':
        data = data[0:len(data) - 1]
    id_curso = DC_Sinonimo.getIdCurso(connection, data.upper())
    if id_curso != 0:
        resp = DC_Curso.getCursoDescription(connection, id_curso["id_curso_sin"])
        return resp
    else:
        return 0


def getCursoPrerequisitos(connection, data):
    if data[0] == ' ':
        data = data[1:len(data)]
    if data[len(data) - 1] == ' ':
        data = data[0:len(data) - 1]
    id_curso = DC_Sinonimo.getIdCurso(connection, data.upper())
    if id_curso != 0:
        resp = DC_Curso.getCursoPreRequisitos(connection, id_curso["id_curso_sin"])
        return resp
    else:
        return 0
