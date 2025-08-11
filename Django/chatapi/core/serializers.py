from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from django.contrib.auth.hashers import check_password
from .models import User, AuthToken


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["username", "password"]

    def validate_username(self, value: str) -> str:
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        # tokens default is 4000 via model default
        return super().create(validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")
        if not check_password(password, user.password):
            raise serializers.ValidationError("Invalid credentials")
        attrs["user"] = user
        return attrs


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField()
    # Allow token in body as a fallback to Authorization header
    token = serializers.CharField(required=False, write_only=True)




