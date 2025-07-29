from rest_framework import serializers

from app.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'surname', 'phone', 'subscribe']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    name = serializers.CharField(required=False)
    surname = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    subscribe = serializers.BooleanField(required=False, default=False)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class CheckAuthResponseSerializer(serializers.Serializer):
    is_authenticated = serializers.BooleanField()
    id = serializers.IntegerField(required=False)
    email = serializers.EmailField(required=False)
    name = serializers.CharField(required=False)
    surname = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    subscribe = serializers.BooleanField(required=False)


class SuccessResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()


class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField()


class EmailVerifiedResponseSerializer(serializers.Serializer):
    is_verified = serializers.BooleanField()
