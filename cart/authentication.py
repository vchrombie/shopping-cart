import jwt

from rest_framework import authentication, exceptions
from rest_framework.exceptions import AuthenticationFailed

from django.contrib.auth import get_user_model

from cart.models import TempUser

User = get_user_model()


class CustomAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        request.user = None

        token = request.headers.get('Authorization').split()[-1]

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        response = {
            "id": payload['id'],
        }

        try:
            user = TempUser(**response)
        except TempUser.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise AuthenticationFailed(msg)

        return user, token
