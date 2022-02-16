import json

import requests
from rest_framework import viewsets, permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

import cart.authentication
from .models import Category, Product, Cart, TempUser
from .serializers import CategorySerializer, ProductSerializer, CartSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = Product.objects.all().order_by('category_id')
    serializer_class = ProductSerializer


class CartView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request):
        cart_obj = Cart.objects.all().filter(user_id__exact=request.user.id)
        serializer = CartSerializer(cart_obj, many=True)
        return Response(serializer.data)


class LoginView(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    authentication_classes = []

    def post(self, request):
        phone_number = request.data['phone_number']
        password = request.data['password']

        data = json.dumps({
            "phone_number": phone_number,
            "password": password
        })
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.request(
            "POST",
            "http://localhost:8000/api/login/",
            headers=headers,
            data=data
        )

        token = response.json()['jwt']

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            "jwt": token,
        }
        return response
