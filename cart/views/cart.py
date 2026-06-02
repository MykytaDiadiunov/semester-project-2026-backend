from http import HTTPMethod

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.viewsets import GenericViewSet

from cart.execeptions.cart import CartNoItemsError
from cart.models.cart import Cart
from cart.serializers.cart import AddItemSerializer, ReadCartSerializer
from cart.services.cart import CartService


class CartViewSet(GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = ReadCartSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=[HTTPMethod.POST.value], detail=False, url_path="manage-item")
    def manage_item(self, request):
        request_serializer = AddItemSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        validated_data = request_serializer.validated_data
        cart_service = CartService(request.user)

        cart = cart_service.manage_cart_item(validated_data)

        return Response(self.serializer_class(cart).data, status=status.HTTP_201_CREATED)

    @action(methods=[HTTPMethod.PATCH.value], detail=False, url_path="close-cart-order")
    def close_cart_order(self, request):
        cart_service = CartService(request.user)

        try:
            cart_service.close_cart_order()
            return Response(status=status.HTTP_202_ACCEPTED)
        except CartNoItemsError as e:
            return Response(data={"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
