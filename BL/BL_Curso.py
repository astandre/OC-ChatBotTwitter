from DC import DC_Sinonimo, DC_Curso
import unicodedata

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
def getProfesor(connection, data):
    new_data = cleanData(data)
    id_curso = DC_Sinonimo.getIdCurso(connection, new_data.upper())
    if id_curso != 0:
        resp = DC_Curso.getProfesor(connection, id_curso["id_curso_sin"])
        return resp
    else:
        return 0


def cleanData(data):
    articles = ["el", "y", "la", "los", "tu","las","de",
                "EL","Y","LA","LOS","TU","LAS","DE"]
    special = ["¿", "?", "!","¡","(",")",",",".",";",":","-","-","{","}","[","]","+","-","/","*","<",">"]
    data_aux = ""
    for i in range(0, len(data) ):
        if i + 1 <= len(data) -1:
            if data[i] not in special:
                if data[i] == " ":
                    if data[i+1] != " ":
                        data_aux = data_aux + data[i]
                else:
                    data_aux = data_aux + data[i]
    words = data_aux.split(" ")
    new_data = ""
    for word in words:
        if word not in articles:
            if word[0] != "@" and word[0] != "#":
                new_data = new_data + " " + word
    if new_data[0] == ' ':
        new_data = new_data[1:len(new_data)]
    if new_data[len(new_data) - 1] == ' ':
        new_data = new_data[0:len(new_data) - 1]
    return strip_accents(new_data)

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')