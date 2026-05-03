from rest_framework import viewsets

from core.pagination import BasePagination
from product.models.product import Product
from product.serializers.product import ProductSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = BasePagination
