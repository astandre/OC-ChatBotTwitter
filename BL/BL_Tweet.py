from DC import DC_Tweets


def insertTweet(connection, name, text, tweet):
    resp = DC_Tweets.insertTweet(connection, name, text, tweet)
    if resp != 0:
        return resp
    else:
        return 0
