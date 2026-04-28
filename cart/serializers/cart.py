from rest_framework import serializers

from cart.models.cart import Cart, CartItem
from product.models.product import Product
from user.serializers.user import CompactUserSerializer


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            "product",
            "quantity",
        ]


class ReadCartSerializer(serializers.ModelSerializer):
    user = CompactUserSerializer(read_only=True)
    items = CartItemSerializer(source="cart_items", read_only=True, many=True)

    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "status",
            "items",
        ]


class AddItemSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField()
