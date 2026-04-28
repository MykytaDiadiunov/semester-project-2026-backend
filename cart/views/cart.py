from http import HTTPMethod

from django.db import transaction
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.viewsets import GenericViewSet

from cart.models.cart import Cart, CartItem, CartStatusChoice
from cart.serializers.cart import AddItemSerializer, ReadCartSerializer


class CartViewSet(GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = ReadCartSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=[HTTPMethod.POST.value], detail=False)
    def add_item(self, request):
        request_serializer = AddItemSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        data = request_serializer.validated_data
        product = data["product"]
        quantity = data["quantity"]

        with transaction.atomic():
            cart, _ = Cart.objects.get_or_create(
                user=request.user,
                status=CartStatusChoice.ACTIVE,
            )
            if quantity > 0:
                CartItem.objects.update_or_create(cart=cart, product=product, defaults={"quantity": quantity})
            else:
                CartItem.objects.filter(cart=cart, product=product).delete()

        return Response(ReadCartSerializer(cart).data, status=status.HTTP_201_CREATED)
