from DC import DC_FAQ


def getRespuesta(connection, data):
    if data[0] == ' ':
        data = data[1:len(data)]
    if data[len(data) - 1] == ' ':
        data = data[0:len(data) - 1]
    resp = DC_FAQ.getRespuesta(connection, data)
    if resp != 0:
        return resp
    else:
        return 0
