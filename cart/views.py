from django.contrib.auth import get_user_model

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Product, Cart
from .serializers import CategorySerializer, ProductSerializer, CartSerializer
from .helpers import CartHelper

User = get_user_model()


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all().order_by('category_id')
    serializer_class = ProductSerializer


class CartViewSet(viewsets.ModelViewSet):

    serializer_class = CartSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        return Cart.objects.all().order_by('-id').filter(user=self.request.user)

    @action(
        methods=['GET'],
        detail=False,
        url_name='checkout',
        url_path='checkout/<int"pk>/',
    )
    def checkout(self, request, *args, **kwargs):

        try:
            user = User.objects.get(pk=int(kwargs.get('userId')))
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'Error:': str(e)})

        cart_helper = CartHelper(user)
        checkout_details = cart_helper.prepare_cart_for_checkout()

        if not checkout_details:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'Error': "Cart is empty!"})

        return Response(status=status.HTTP_200_OK,
                        data={'checkout_details': checkout_details})
