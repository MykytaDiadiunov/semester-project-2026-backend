from django.db import transaction

from cart.execeptions.cart import CartNoItemsError
from cart.models.cart import Cart, CartItem, CartStatusChoice


class CartService:
    def __init__(self, user):
        self.user = user

    def manage_cart_item(self, validated_item_data):
        product = validated_item_data["product"]
        quantity = validated_item_data["quantity"]

        with transaction.atomic():
            cart, _ = Cart.objects.get_or_create(
                user=self.user,
                status=CartStatusChoice.ACTIVE,
            )
            if quantity > 0:
                CartItem.objects.update_or_create(cart=cart, product=product, defaults={"quantity": quantity})
            else:
                CartItem.objects.filter(cart=cart, product=product).delete()

        return cart

    def close_cart_order(self):
        cart = self.user.carts.get(status=CartStatusChoice.ACTIVE)

        if not cart.cart_items.exists():
            raise CartNoItemsError()

        cart.status = CartStatusChoice.FINISHED
        cart.save(update_fields=["status"])
