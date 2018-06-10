from DC import DC_Tweets


def insertTweet(connection, name, created_at, usuario, text, source, location, tweet):
    resp = DC_Tweets.insertTweet(connection, name, created_at, usuario, text, source, location, tweet)
    if resp != 0:
        return resp
    else:
        return 0
