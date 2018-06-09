
def getIdCurso(cn, name):
    try:
        with cn.cursor() as cursor:
            # Read a single record
            sql = "SELECT id_curso_sin FROM sinonimos WHERE sinonimo LIKE '%" + name + "%'"
            if cursor.execute(sql) != 0:
                result = cursor.fetchone()
                return result
            else:
                return 0
    except Exception:
        print("error", Exception)