from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import ValidationError

from users.models import CustomUser


class CustomUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class CustomUserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_email(self, value: str) -> str:
        if CustomUser.objects.filter(email=value).exists():
            raise ValidationError('User with this email already exists')
        return value

    def create(self, validated_data: dict) -> CustomUser:
        email = validated_data['email']
        password = validated_data['password1']
        return CustomUser.objects.create_user(email=email, password=password)

    def validate(self, attrs: dict) -> dict:
        if attrs['password1'] != attrs['password2']:
            raise ValidationError({'password2': 'Not equal passwords'})
        validate_password(password=attrs['password1'])
        return attrs
