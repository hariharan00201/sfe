from itsdangerous import TimedJSONWebSignatureSerializer as serializer


def genarateToken(email):
    s = serializer('sfesecret', 300)
    token = s.dumps({'user_id':email}).decode('utf-8')
    print('token created')
    return token


def verifyToken(token):
    s = serializer('sfesecret')
    try:
        email = s.loads(token)['user_id']
    except:
        return None
    print(email)
    return email