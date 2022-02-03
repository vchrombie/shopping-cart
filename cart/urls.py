from django.urls import path, include

from rest_framework import routers

from .views import CategoryViewSet, ProductViewSet, CartViewSet


router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'', CartViewSet, basename='Cart')

urlpatterns = [
    path('', include((router.urls, 'cart')))
]
