import tweepy
from decouple import config
import pymysql.cursors
import tweepy
import json, time, datetime
from BL import BL_Curso, BL_FAQ, BL_Tweet
import math

# Twitter authentication
auth = tweepy.OAuthHandler(config('API_KEY'), config('API_SECRET'))
auth.set_access_token(config('ACCES_TOKEN'), config('ACCES_TOKEN_SECRET'))

api = tweepy.API(auth)
# Connect to the database
connection = pymysql.connect(host='localhost',
                             user=config('USER'),
                             password=config('DB_PASS'),
                             db=config('DB_NAME'),
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
# Launching App
file_open = open("welcome.txt", "r")
for line in file_open:
    print(line, end="")
file_open.close()
print("\nListening for Tweets @opencampus_go ....")


class StreamListener(tweepy.StreamListener):
    """
    Tweets listener
    """

    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        curso_no_encontrado = "No he podido encontrar el curso, recuerda escribir bien el nombre del curso"
        pregunta_no_encontrada = "No he podido encontrar respuesta a tu pregunta, puedes revisar las preguntas frecuentes para más informacion http://opencampus.utpl.edu.ec/faq"
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print("\n", st, "[DEBUG] (Raw-Tweet): ", data)
        tweet = json.loads(data)
        user = tweet["user"]["screen_name"]
        if BL_Tweet.insertTweet(connection, tweet["user"]["name"], tweet["created_at"], tweet["user"]["screen_name"],
                                tweet["text"], tweet["source"], str(tweet["user"]["location"]), data) != 0:
            # TODO test location
            print(st, "[DEBUG]: Tweet guardado en la Base de datos!")
        else:
            print(st, "[DEBUG]: No se ha podido guardar el tweet")
        print(st, "[Tweet]: ", tweet["text"])
        hash_tags = tweet["entities"]["hashtags"]
        flag = 1
        for hash_tag in hash_tags:
            if hash_tag["text"].upper() == "CURSO" or hash_tag["text"].upper() == "CURSOS":
                flag = 0
                break
        if flag == 0:
            print(st, "[User]: ", user)
            for hash_tag in hash_tags:
                if hash_tag["text"].upper() == "INFORMACION":
                    resp = BL_Curso.getCursoDescripcion(connection, tweet["text"])
                    if resp != 0:
                        size = 280 - (len(user) + len(resp["nombre"]) + len(resp["link"]) + 20)
                        full_response = "Informacíon " + resp["nombre"] + ": " + resp["descripcion"][0:size] + "... " + \
                                        resp["link"]
                        updateStatus(user, full_response)
                    else:
                        print(st, "[DEBUG]: ", "No se ha encontrado ", tweet["text"])
                        updateStatus(user, curso_no_encontrado)
                if hash_tag["text"].upper() == "PRERREQUISITOS":
                    resp = BL_Curso.getCursoPrerequisitos(connection, tweet["text"])
                    if resp != 0:
                        full_response = "Los prerrequisitos para el curso " + resp["nombre"] + " son: " + resp[
                            "pre_requisito"]
                        updateStatus(user, full_response)
                    else:
                        print(st, "[DEBUG]: ", "No se ha encontrado ", tweet["text"])
                        updateStatus(user, curso_no_encontrado)
                if hash_tag["text"].upper() == "FECHA" or hash_tag["text"].upper() == "FECHAS":
                    resp = BL_Curso.getFechas(connection, tweet["text"])
                    if resp != 0:
                        full_response = "La inscripcion al curso " + resp["nombre"] + " comienza el dia " + str(
                            resp["fecha_inscripcion"].strftime(
                                "%d-%m-%Y")) + " y el inicio de actividades es el dia " + str(
                            resp["fecha_inicio"].strftime("%d-%m-%Y"))
                        updateStatus(user, full_response)
                    else:
                        print(st, "[DEBUG]: ", "No se ha encontrado ", tweet["text"])
                        updateStatus(user, curso_no_encontrado)
                if hash_tag["text"].upper() == "DURACION" or hash_tag["text"].upper() == "ESFUERZO" or hash_tag[
                    "text"].upper() == "TIEMPO":
                    resp = BL_Curso.getDuracion(connection, tweet["text"])
                    if resp != 0:
                        full_response = "El curso " + resp["nombre"] + " tiene una duracion de " + str(
                            resp["duracion"]) + " semanas, con un esfuerzo estimado de " + str(
                            resp["esfuerzo_est"]) + " horas por semana"
                        updateStatus(user, full_response)
                    else:
                        print(st, "[DEBUG]: ", "No se ha encontrado ", tweet["text"])
                        updateStatus(user, curso_no_encontrado)
                if hash_tag["text"].upper() == "MATRICULA" or hash_tag["text"].upper() == "INSCRIPCION":
                    resp = BL_Curso.getLink(connection, tweet["text"])
                    if resp != 0:
                        full_response = "Puedes inscribirte al curso " + resp["nombre"] + " en el siguiente enlace: " + \
                                        resp["link"]
                        updateStatus(user, full_response)
                    else:
                        print(st, "[DEBUG]: ", "No se ha encontrado ", tweet["text"])
                        updateStatus(user, curso_no_encontrado)
                if hash_tag["text"].upper() == "DOCENTE" or hash_tag["text"].upper() == "PROFESOR":
                    docentes = BL_Curso.getProfesor(connection, tweet["text"])
                    if docentes != 0:
                        if len(docentes) >= 2:
                            full_response = "Los docentes encargados son "
                            for docente in docentes:
                                full_response = full_response + docente["nombre"] + " (" + docente["email"] + ") "
                        else:
                            if len(docentes[0]["twitter"]) > 0:
                                full_response = "El docente encargado es " + docentes[0]["nombre"] + " (" + docentes[0][
                                    "email"] + ") " + docentes[0]["twitter"]
                            else:
                                full_response = "El docente encargado es " + docentes[0]["nombre"] + " (" + docentes[0][
                                    "email"] + ")"
                        updateStatus(user, full_response)
                    else:
                        print(st, "[DEBUG]: ", "No se ha encontrado ", tweet["text"])
                        updateStatus(user, curso_no_encontrado)
                if hash_tag["text"].upper() == "TEMAS" or hash_tag["text"].upper() == "CONTENIDO" or hash_tag[
                    "text"].upper() == "TEMA":
                    contenidos = BL_Curso.getContenido(connection, tweet["text"])
                    if contenidos != 0:
                        full_response = "Los contenidos del curso " + contenidos[0]["nombre"] + " son "
                        for i in range(0, len(contenidos)):
                            if i + 1 == len(contenidos):
                                full_response = full_response + contenidos[i]["contenido"]
                            else:
                                full_response = full_response + contenidos[i]["contenido"] + ", "
                        updateStatus(user, full_response)
                    else:
                        print(st, "[DEBUG]: ", "No se ha encontrado ", tweet["text"])
                        updateStatus(user, curso_no_encontrado)
                if hash_tag["text"].upper() == "COMPETENCIAS" or hash_tag["text"].upper() == "COMPETENCIA":
                    competencias = BL_Curso.getCompetencias(connection, tweet["text"])
                    if competencias != 0:
                        full_response = "Las competencias a obtener del curso " + competencias[0]["nombre"] + " son "
                        for i in range(0, len(competencias)):
                            if i + 1 == len(competencias):
                                full_response = full_response + competencias[i]["competencia"]
                            else:
                                full_response = full_response + competencias[i]["competencia"] + ", "
                        updateStatus(user, full_response)
                    else:
                        print(st, "[DEBUG]: ", "No se ha encontrado ", tweet["text"])
                        updateStatus(user, curso_no_encontrado)
                if hash_tag["text"].upper() == "RETOS" or hash_tag["text"].upper() == "RETO":
                    #             TODO consultar data de retos
                    resp = BL_Curso.getRetos(connection, tweet["text"])
                    if resp != 0:
                        if len(resp) >= 2:
                            full_response = "Los retos de " + resp[0]["nombre"] + " son "
                        else:
                            full_response = "El reto de " + resp[0]["nombre"] + " es "
                        for i in range(0, len(resp)):
                            if i + 1 == len(resp):
                                full_response = full_response + resp[i]["descripcion"] + " (" + resp[i][
                                    "fecha_entrega"].strftime("%d-%m-%Y") + ")"
                            else:
                                full_response = full_response + resp[i]["descripcion"] + " (" + resp[i][
                                    "fecha_entrega"].strftime("%d-%m-%Y") + ") , "
                        updateStatus(user, full_response)
                    else:
                        print(st, "[DEBUG]: ", "No se ha encontrado ", tweet["text"])
        else:
            print(st, "[User]: ", user)
            print(st, "[Question]: ", tweet["text"])
            resp = BL_FAQ.getRespuesta(connection, tweet["text"])
            if resp != 0:
                size = 280 - (len(user) + len(resp["link"]) + 16)
                full_response = resp["respuesta"][0:size] + "... " + resp["link"]
                updateStatus(user, full_response)
            else:
                print(st, "[DEBUG]: ", "No se ha encontrado ", tweet["text"])
                updateStatus(user, pregunta_no_encontrada)

        return True

    def on_error(self, status):
        print(status)


def updateStatus(user, response):
    """
    Updates user status
    :param user: name of the twitter user
    :param response: response intended to be published
    :return:
    """
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    full_response = ""  # ""@" + user + " " + response
    size = len(response) + len(user)
    if size >= 280:
        print(st, "[DEBUG]: El tweet supera el maximo de caracteres, dividinedo respuesta!")
        parts = response.split(" ")
        size_parts = int(math.ceil(size / 280))
        plus = len(parts) // size_parts
        inicio = 0
        fin = plus
        for x in range(0, size_parts):
            full_response = "@" + user + " " + str(x + 1) + "."
            for i in range(inicio, fin):
                full_response = full_response + " " + parts[i]
            if x + 1 != size_parts:
                full_response = full_response + " ..."
            inicio = fin
            fin = fin + plus
            try:
                full_response = full_response + " #BOT "
                if api.update_status(full_response):
                    print(st, "[Response]: (", str(len(full_response)), ") ", full_response)
            except tweepy.error.TweepError as e:
                print(st, "[DEBUG]: El post ya existe ...  ")
    else:
        full_response = "@" + user + " " + response
        try:
            full_response = full_response + " #BOT"
            if api.update_status(full_response):
                print(st, "[Response]: (", str(len(full_response)), ") ", full_response)
        except tweepy.error.TweepError as e:
            print(st, "[DEBUG]: El post ya existe ...  ")
            # response = response + " ..."
            # updateStatus(user, response)


myStreamListener = StreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(follow=[config('MY_ID')], async=True)
# @testmiller33 #Prerrequisitos #Curso Manejo y Exploración de Datos
# @testmiller33 #RETOS #Curso Manejo y Exploración de Datos
# @testmiller33 #Informacion #Curso Manejo y Exploración de Datos
# @testmiller33 #Profesor #curso Emprendimiento y generación de ideas
# @testmiller33 #Temas #curso Emprendimiento y generación de ideas
# @testmiller33 #COMPETENCIAS #curso Emprendimiento y generación de ideas
# @testmiller33 #RETO #curso Emprendimiento y generación de ideas
# @testmiller33 #MATRICULA #curso Emprendimiento y generación de ideas
# @testmiller33 #DURACION #curso Emprendimiento y generación de ideas
# @testmiller33 ¿Cómo puedo inscribirme?
# @testmiller33 ¿Como funciona el bot?
# @testmiller33 #Fecha #Curso Manejo Datos
