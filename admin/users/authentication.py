import jwt
import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


def generate_access_token(user):
    issued_at = datetime.datetime.utcnow()
    expiration = issued_at + datetime.timedelta(minutes=60)
    payload = {
        'user_id': user.id,
        'exp': expiration.timestamp(),
        'iat': issued_at.timestamp()
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('jwt')
        print('token::',token)
        if not token:
            return None
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('unauthenticated')

        user = get_user_model().objects.filter(id=payload['user_id']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found!')
        return (user, None)

