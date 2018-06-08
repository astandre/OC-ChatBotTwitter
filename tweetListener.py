import tweepy
from decouple import config
import pymysql.cursors
import tweepy
import json, time, datetime
from BL import BL_Curso, BL_FAQ, BL_Tweet

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
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print("\n", st, "[DEBUG] (Raw-Tweet): ", data)
        tweet = json.loads(data)
        user = tweet["user"]["screen_name"]
        if BL_Tweet.insertTweet(connection, user, tweet["text"], data) != 0:
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
                        full_response = "El curso " + resp["nombre"] + " trata: " + resp["descripcion"]
                        print(st, "[Response]: ", full_response)
                        updateStatus(user, full_response)
                    else:
                        print(st, "[DEBUG]: ", "No se ha encontrado ", tweet["text"])
                if hash_tag["text"].upper() == "PRERREQUISITOS":
                    resp = BL_Curso.getCursoPrerequisitos(connection, tweet["text"])
                    if resp != 0:
                        full_response = "Los prerrequisitos para el curso " + resp["nombre"] + " son: " + resp[
                            "pre_requisito"]
                        updateStatus(user, full_response)
                        print(st, "[Response]: ", full_response)
                    else:
                        print(st, "[DEBUG]: ", "No se ha encontrado ", tweet["text"])
                if hash_tag["text"].upper() == "FECHA" or hash_tag["text"].upper() == "FECHAS":
                    resp = BL_Curso.getFechas(connection, tweet["text"])
                    if resp != 0:
                        full_response = "La inscripcion al curso " + resp["nombre"] + " comienza el dia " + str(
                            resp["fecha_inscripcion"].strftime(
                                "%d-%m-%Y")) + " el inicio de actividades es el dia: " + str(
                            resp["fecha_inicio"].strftime("%d-%m-%Y"))
                        updateStatus(user, full_response)
                        print(st, "[Response]: ", full_response)
                    else:
                        print(st, "[DEBUG]: ", "No se ha encontrado ", tweet["text"])
                if hash_tag["text"].upper == "DURACION" or hash_tag["text"].upper == "ESFUERZO":
                    #             TODO FINISH
                    resp = BL_Curso.getCursoPrerequisitos(connection, tweet["text"])
                    if resp != 0:
                        print(st, "[Response]: ", resp["pre_requisito"])
                    else:
                        print(st, "[DEBUG]: ", "No se ha encontrado ", tweet["text"])
                if hash_tag["text"].upper == "LINK" or hash_tag["text"].upper == "INSCRIPCION":
                    #             TODO FINISH
                    resp = BL_Curso.getCursoPrerequisitos(connection, tweet["text"])
                    if resp != 0:
                        print(st, "[Response]: ", resp["pre_requisito"])
                    else:
                        print(st, "[DEBUG]: ", "No se ha encontrado ", tweet["text"])
                if hash_tag["text"].upper == "DOCENTE" or hash_tag["text"].upper == "PROFESOR":
                    #             TODO FINISH
                    resp = BL_Curso.getCursoPrerequisitos(connection, tweet["text"])
                    if resp != 0:
                        print(st, "[Response]: ", resp["pre_requisito"])
                    else:
                        print(st, "[DEBUG]: ", "No se ha encontrado ", tweet["text"])
                if hash_tag["text"].upper == "TEMAS" or hash_tag["text"].upper == "CONTENIDO":
                    #             TODO FINISH
                    resp = BL_Curso.getCursoPrerequisitos(connection, tweet["text"])
                    if resp != 0:
                        print(st, "[Response]: ", resp["pre_requisito"])
                    else:
                        print(st, "[DEBUG]: ", "No se ha encontrado ", tweet["text"])
                if hash_tag["text"].upper == "COMPETENCIAS" or hash_tag["text"].upper == "COMPETENCIA":
                    #             TODO FINISH
                    resp = BL_Curso.getCursoPrerequisitos(connection, tweet["text"])
                    if resp != 0:
                        print(st, "[Response]: ", resp["pre_requisito"])
                    else:
                        print(st, "[DEBUG]: ", "No se ha encontrado ", tweet["text"])
                if hash_tag["text"].upper == "RETOS" or hash_tag["text"].upper == "RETO":
                    #             TODO FINISH
                    resp = BL_Curso.getCursoPrerequisitos(connection, tweet["text"])
                    if resp != 0:
                        print(st, "[Response]: ", resp["pre_requisito"])
                    else:
                        print(st, "[DEBUG]: ", "No se ha encontrado ", tweet["text"])
        else:
            print(st, "[User]: ", user)
            question = tweet["text"][tweet['text'].find('¿'):tweet['text'].find('?') + 1]
            print(st, "[Question]: ", question)
            resp = BL_FAQ.getRespuesta(connection, question)
            if resp != 0:
                updateStatus(user, resp)
                print(st, "[Response]: ", resp)
            else:
                print(st, "[DEBUG]: ", "No se ha encontrado ", question)

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
    # TODO make mutiple tweets if user name is very large
    full_response = "@" + user + " " + response
    if len(full_response) > 280:
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print(st, "[DEBUG]: El tweet supera el maximo de caracteres!")
        # print(full_response)
    else:
        api.update_status(full_response)


myStreamListener = StreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(follow=[config('MY_ID')], async=True)
# @testmiller33 #Prerrequisitos #Curso Manejo y Exploración de Datos
# @testmiller33 #Informacion #Curso Manejo y Exploración de Datos
# @testmiller33  ¿Cómo puedo inscribirme?
# @testmiller33 #Fecha #Curso Manejo y Exploración de Datos
