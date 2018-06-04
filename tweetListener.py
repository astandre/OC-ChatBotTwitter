import tweepy
from decouple import config
import pymysql.cursors
import tweepy
import json, time, datetime
from DC import DC_FAQ, DC_Curso

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
print("\nListening for Tweets @opencampus_go\n")


class StreamListener(tweepy.StreamListener):
    """
    Tweets listener
    """

    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print(st, "[DEBUG]: ", data)
        tweet = json.loads(data)
        print(st, "[Tweet]: ", tweet["text"])
        user = tweet["user"]["screen_name"]
        hash_tags = tweet["entities"]["hashtags"]
        flag = 1
        for hash_tag in hash_tags:
            if hash_tag["text"].upper() == "CURSO" or hash_tag["text"].upper() == "CURSOS":
                flag = 0
                break
        if flag == 0:
            name = tweet["text"][tweet['text'].find(':') + 1:len(tweet['text']) + 1]
            for hash_tag in hash_tags:
                if hash_tag["text"].upper() == "INFORMACION":
                    resp = DC_Curso.getCursoDescription(connection, name)
                    print(st, "[Response]: ", resp["descripcion"])
                if hash_tag["text"].upper() == "PREREQUISITOS":
                    resp = DC_Curso.getCursoPreRequisitos(connection, name)
                    print(st, "[Response]: ", resp["pre_requisito"])
        else:
            print(st, "[User]: ", user)
            question = tweet["text"][tweet['text'].find('¿'):tweet['text'].find('?') + 1]
            print(st, "[Question]: ", question)
            resp = DC_FAQ.getRespuesta(connection, question)
            updateStatus(user, resp)
            print(st, "[Response]: ", resp)

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
        print("Alerta supera el maximo")
        print(full_response)
    else:
        api.update_status(full_response)


myStreamListener = StreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(follow=[config('MY_ID')], async=True)
# @testmiller33 #Prerequisitos #Curso : Manejo y Exploración de Datos
# @testmiller33 #Informacion #Curso : Manejo y Exploración de Datos
# @testmiller33  ¿Cómo puedo inscribirme?
