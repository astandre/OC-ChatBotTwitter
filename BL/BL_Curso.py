from DC import DC_Sinonimo, DC_Curso


def getCursoDescripcion(connection, data):
    new_data = cleanData(data)
    id_curso = DC_Sinonimo.getIdCurso(connection, new_data.upper())
    if id_curso != 0:
        resp = DC_Curso.getCursoDescription(connection, id_curso["id_curso_sin"])
        return resp
    else:
        return 0


def getCursoPrerequisitos(connection, data):
    new_data = cleanData(data)

    id_curso = DC_Sinonimo.getIdCurso(connection, new_data.upper())
    if id_curso != 0:
        resp = DC_Curso.getCursoPreRequisitos(connection, id_curso["id_curso_sin"])
        return resp
    else:
        return 0


def getFechas(connection, data):
    new_data = cleanData(data)
    id_curso = DC_Sinonimo.getIdCurso(connection, new_data.upper())
    if id_curso != 0:
        resp = DC_Curso.getFechas(connection, id_curso["id_curso_sin"])
        return resp
    else:
        return 0


def cleanData(data):
    words = data.split(" ")
    new_data = ""
    for word in words:
        if word[0] != "@" and word[0] != "#":
            new_data = new_data + " " + word
    if new_data[0] == ' ':
        new_data = new_data[1:len(new_data)]
    if new_data[len(new_data) - 1] == ' ':
        new_data = new_data[0:len(new_data) - 1]
    return new_data
