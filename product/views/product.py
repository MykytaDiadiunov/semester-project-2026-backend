from rest_framework import viewsets

from product.models.product import Product
from product.serializers.product import ProductSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
