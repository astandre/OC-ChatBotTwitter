
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
