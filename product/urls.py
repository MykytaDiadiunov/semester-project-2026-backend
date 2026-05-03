from django.urls import path
from rest_framework import routers

from product.views.product import ProductViewSet

router = routers.SimpleRouter()

router.register("", ProductViewSet, basename="products")

urlpatterns = []

urlpatterns += router.urls
