from django.contrib.auth import get_user_model
from rest_framework import serializers

BASE_USER_FIELDS = ["id", "username", "email", "first_name", "last_name"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [*BASE_USER_FIELDS, "auth_token"]


class CompactUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [*BASE_USER_FIELDS]
