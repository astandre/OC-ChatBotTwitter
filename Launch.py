from decouple import config
import tweepy
import json
import math
import logging
from services import *
import constants


class StreamListener(tweepy.StreamListener):
    """
    Tweets listener
    """

    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        logger.info(data)
        tweet = json.loads(data)
        name = tweet["user"]["name"]
        user_name = tweet["user"]["screen_name"]
        content = tweet["text"]
        hash_tags = tweet["entities"]["hashtags"]
        id_account = tweet["user"]["id"]
        tweet_id = tweet["id"]
        data = {"user_name": user_name, "content": content, "name": name, "id_account": id_account}
        if len(hash_tags) > 0:
            # TODO handle multiple hashtags
            data.update(
                {"command": {"begin": hash_tags[0]["indices"][0], "end": hash_tags[0]["indices"][1]}})
        resp = chat_with_system(data)
        if resp is not None:
            update_status(user_name, tweet_id, str(resp["output"]))
        else:
            logger.error("Error")
            update_status(user_name, tweet_id, constants.ERROR)

    def on_error(self, status):
        print(status)


def update_status(user, tweet_id, response):
    """
    Updates user status
    :param user: name of the twitter user
    :param tweet_id: id of tweet
    :param response: response intended to be published
    :return:
    """
    size = len(response)  # + len(user)
    if size >= 280:
        logger.info("El tweet supera el maximo de caracteres, dividinedo respuesta!")
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
                if api.update_status(full_response, tweet_id):
                    log_resp = str(len(full_response)) + " - " + str(full_response)
                    logger.info(log_resp)
            except tweepy.error.TweepError as e:
                logger.info("El post ya existe ... ")
    else:
        full_response = "@" + user + " " + response
        try:
            full_response = full_response
            if api.update_status(full_response, tweet_id):
                log_resp = str(len(full_response)) + " - " + str(full_response)
                logger.info(log_resp)
        except tweepy.error.TweepError as e:
            logger.info("El post ya existe ... ")


def update_status_media(file, user, user_id, response):
    try:
        full_response = "@" + user + " " + response
        if api.update_with_media(file, full_response, in_reply_to_status_id=user_id):
            logger.info(str(len(full_response)), ") ", full_response)
    except tweepy.error.TweepError as e:
        logger.error("El post ya existe ... ")


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    # Launching App
    file_open = open("welcome.txt", "r")
    for line in file_open:
        print(line, end="")
    file_open.close()
    commands = init_chatbot()
    if commands is None:
        logger.info("Error al inicializar el bot")
    else:
        COMANDOS_DISPONIBLES = commands["simple"]
        COMANDOS_DISPONIBLES_FULL = commands["full"]
        print(COMANDOS_DISPONIBLES_FULL)
        print(COMANDOS_DISPONIBLES)
        # Twitter authentication
        auth = tweepy.OAuthHandler(config('API_KEY'), config('API_SECRET'))
        auth.set_access_token(config('ACCES_TOKEN'), config('ACCES_TOKEN_SECRET'))

        api = tweepy.API(auth)
        myStreamListener = StreamListener()
        myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener, async=True)
        if config('DEBUG', default=False, cast=bool):
            print("\nListening for Tweets @testmiller33 ....")
            myStream.filter(follow=[config('MY_ID')], async=True)
        else:
            print("\nListening for Tweets @opencampus_go ....")
            myStream.filter(follow=[config('OC_ID')], async=True)

# @testmiller33 #Prerrequisitos #info Manejo y Exploración de Datos
# @testmiller33 #RETOS  Manejo y Exploración de Datos
# @testmiller33 #Info  Manejo datos
# @testmiller33 #Informacion  Manejo y Exploración de Datos
# @testmiller33 #Profesor  Emprendimiento y generación de ideas
# @testmiller33 #Temas Emprendimiento y generación de ideas
# @testmiller33 #COMPETENCIAS Emprendimiento y generación de ideas
# @testmiller33 #RETO Emprendimiento y generación de ideas
# @testmiller33 #MATRICULA Emprendimiento y generación de ideas
# @testmiller33 #DURACION Emprendimiento y generación de ideas
# @testmiller33 ¿Cómo puedo inscribirme?
# @testmiller33 ¿Como funciona el bot?
# @testmiller33 #Fecha #Curso Manejo Datos
