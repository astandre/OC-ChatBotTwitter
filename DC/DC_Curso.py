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


def getCursoDescription(cn, name):
    try:
        with cn.cursor() as cursor:
            # Read a single record
            sql = "SELECT descripcion FROM curso WHERE descripcion LIKE '%" + name + "%'"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result
    except Exception:
        print("error", Exception)

def getCursoPreRequisitos(cn, name):
    try:
        with cn.cursor() as cursor:
            # Read a single record
            sql = "SELECT pre_requisito FROM curso WHERE descripcion LIKE '%" + name + "%'"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result
    except Exception:
        print("error", Exception)
