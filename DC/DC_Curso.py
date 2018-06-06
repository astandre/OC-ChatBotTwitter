from MODEL import Curso


def getAllCursos(cn):
    cursos_list = []
    try:
        with cn.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM curso "
            cursor.execute(sql)
            result = cursor.fetchall()
            for res in result:
                curso = Curso.Curso(res["id_curso"], res["nombre"], res["descripcion"])
                cursos_list.append(curso)
    except Exception:
        print("error", Exception)


def getCursoDescription(cn, id_curso):
    try:
        with cn.cursor() as cursor:
            # Read a single record
            sql = "SELECT descripcion FROM curso WHERE id_curso = " + str(id_curso)
            if cursor.execute(sql) != 0:
                result = cursor.fetchone()
                return result
            else:
                return 0
    except Exception:
        print("error", Exception)


def getCursoPreRequisitos(cn, id_curso):
    try:
        with cn.cursor() as cursor:
            # Read a single record
            sql = "SELECT pre_requisito FROM curso WHERE id_curso = " + str(id_curso)
            if cursor.execute(sql) != 0:
                result = cursor.fetchone()
                return result
            else:
                return 0
    except Exception:
        print("error", Exception)
