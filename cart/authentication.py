import jwt
import requests
import json

from rest_framework import authentication, exceptions
from rest_framework.exceptions import AuthenticationFailed

from .models import TempUser


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        request.user = None

        token = request.COOKIES.get('access_token')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            data = json.dumps({
                "phone_number": "+918186866445",
                "password": "root"
            })
            headers = {
                'Content-Type': 'application/json',
            }
            response = requests.request(
                "POST",
                "http://localhost:8000/api/token/",
                headers=headers,
                data=data
            )

            token = response.json()['access']

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            data = {}
            headers = {
                'Authorization': 'Bearer {}'.format(token),
            }

            response = requests.request(
                "GET",
                "http://localhost:8000/api/user/",
                headers=headers,
                data=data
            )

            print(response.json())
        except Exception as e:
            raise e

        try:
            user = TempUser(**response.json())
        except TempUser.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)

        return user, token
