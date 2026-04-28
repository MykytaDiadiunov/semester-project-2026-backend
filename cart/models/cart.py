from django.conf import settings
from django.db import models


class CartStatusChoice(models.TextChoices):
    ACTIVE = "active", "Active"
    FINISHED = "finished", "Finished"


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length=50,
        choices=CartStatusChoice.choices,
        default=CartStatusChoice.ACTIVE,
    )
    items = models.ManyToManyField("product.Product", through="cart.CartItem", related_name="carts")

    def __str__(self):
        return f"Cart {self.id} for {self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey("cart.Cart", on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart {self.cart.id}"
