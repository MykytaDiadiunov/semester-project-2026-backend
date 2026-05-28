from http import HTTPMethod

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.viewsets import ModelViewSet

from cart.models.cart import Cart, CartStatusChoice
from cart.serializers.cart import ReadCartSerializer
from user.serializers.user import CompactUserSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CompactUserSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=[HTTPMethod.DELETE.value], detail=False)
    def logout(self, request, *args, **kwargs):
        user = request.user
        try:
            Token.objects.get(user=user).delete()
            return Response(status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response(
                {"error": "Token does not exists"},
                status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
            )

    @action(methods=[HTTPMethod.GET.value], detail=False)
    def current(self, request, *args, **kwargs):
        return Response(UserSerializer(request.user).data)

    @action(methods=[HTTPMethod.GET.value], detail=False)
    def cart(self, request, *args, **kwargs):
        user = request.user
        cart, _ = Cart.objects.get_or_create(
            user=user,
            status=CartStatusChoice.ACTIVE,
        )

        return Response(ReadCartSerializer(cart).data, status=status.HTTP_200_OK)
