
def insertTweet(cn, name, created_at, usuario, text, source, location, tweet):
    """
    :param cn: Database connection
    :param data: data to be entered
    :return:
    """

    try:
        with cn.cursor() as cursor:
            # Read a single record
            sql = "INSERT INTO `tweets`( `nombre`, `created_at`, `usuario`, `texto`, `source`, `location`, `raw_tweet`) VALUES ('" + name + "','" + created_at + "','" + usuario + "','" + text + "','" + source + "','" + location + "','" + tweet + "')"
            cursor.execute(sql)
            cn.commit()
    except:
        print("error")

def getLastTweetId(cn):
    try:
        with cn.cursor() as cursor:
            sql = "SELECT id_tweet FROM tweets ORDER BY id_tweet DESC LIMIT 1"
            if cursor.execute(sql) != 0:
                result = cursor.fetchone()
                return result
            else:
                return 0
    except Exception:
        print("error", Exception)

def updateTweetResp(cn,id_tweet):

    try:
        with cn.cursor() as cursor:
            # Read a single record
            sql = " UPDATE `tweets`  SET `respuesta` = 1  WHERE  id_tweet =" + str(id_tweet)
            cursor.execute(sql)
            cn.commit()
    except:
        print("error")