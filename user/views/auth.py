from django.db import transaction
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView, status

from user.serializers.auth import RegisterUserSerializer
from user.serializers.user import UserSerializer


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        obtain_serialized_data = self.serializer_class(data=request.data, context={"request": request})
        obtain_serialized_data.is_valid(raise_exception=True)
        user = obtain_serialized_data.validated_data["user"]
        if user is not None:
            Token.objects.get_or_create(user=user)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        else:
            return Response(obtain_serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serialized_user = RegisterUserSerializer(data=request.data)
        if serialized_user.is_valid():
            user = serialized_user.save()
            Token.objects.get_or_create(user=user)
            return Response({"user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_user.errors, status=status.HTTP_400_BAD_REQUEST)
