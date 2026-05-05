from http import HTTPMethod

from django.db.models import Max, Min
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.pagination import BasePagination
from product.models.product import Product, ProductCategory
from product.serializers.product import ProductCategorySerializer, ProductSerializer


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = BasePagination

    @action(detail=False, methods=[HTTPMethod.GET.value]])
    def filters(self, request):
        categories = ProductCategory.objects.all()
        price_stats = Product.objects.aggregate(min_price=Min("price"), max_price=Max("price"))

        filter_fields = {
            "categories": ProductCategorySerializer(categories, many=True).data,
            "price_range": {
                "min": price_stats["min_price"] or 0,
                "max": price_stats["max_price"] or 0,
            },
        }

        return Response(filter_fields, status=status.HTTP_200_OK)
