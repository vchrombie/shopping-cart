import jwt

from django.conf import settings

from rest_framework import authentication, exceptions
from rest_framework.exceptions import AuthenticationFailed

from django.contrib.auth import get_user_model
User = get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        request.user = None

        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)

        return user, token



