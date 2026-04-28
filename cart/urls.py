from django.urls import path
from rest_framework import routers

from cart.views.cart import CartViewSet

router = routers.SimpleRouter()

router.register("", CartViewSet, basename="cart")

urlpatterns = []

urlpatterns += router.urls
