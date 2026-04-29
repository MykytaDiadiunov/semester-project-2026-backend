from rest_framework import serializers

from product.models.product import Product, ProductCategory

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = [
            "id",
            "name"
        ]


class ProductSerializer(serializers.ModelSerializer):
    category_detail = ProductCategorySerializer(source='category', read_only = True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "category",
            "category_detail"
        ]
        

