def insertTweet(cn, name, text, tweet):
    """

    :param cn: Database connection
    :param data: data to be entered
    :return:
    """

    try:
        with cn.cursor() as cursor:
            # Read a single record
            sql = "INSERT INTO `tweets`( `usuario`, `texto`, `raw_tweet`) VALUES ('" + name + "','" + text + "','" + tweet + "')"
            cursor.execute(sql)
            cn.commit()

    except:
        print("error")
