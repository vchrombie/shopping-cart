from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Product, Cart
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
        cart = Cart.objects.all().filter(user_id__exact=request.user.id)
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data)
