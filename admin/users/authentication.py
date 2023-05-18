import jwt
import datetime
from django.conf import settings

def generate_access_token(user):
    payload = {
        'user_id': user.id,
        'exep': (datetime.datetime.utcnow() + datetime.timedelta(minutes=60)).strftime('%Y-%m-%d %H:%M:%S'),
        'iat': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

