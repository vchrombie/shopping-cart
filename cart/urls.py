from django.urls import path, include

from rest_framework import routers

from .views import CategoryViewSet, ProductViewSet, CartView, LoginView


router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include((router.urls, 'cart'))),
    path('view/', CartView.as_view(), name='cart_view'),
    path('login/', LoginView.as_view(), name='cart_view'),
]
