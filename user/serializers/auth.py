from django.contrib.auth import get_user_model
from rest_framework import serializers


class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        new_user = get_user_model().objects.create_user(**validated_data)
        return new_user
