from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework.validators import ValidationError

from users.models import CustomUser, ResetUserPasswordCode


class CustomUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class CustomUserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def create(self, validated_data: dict) -> CustomUser:
        email = validated_data['email']
        password = validated_data['password1']
        return CustomUser.objects.create_user(email=email, password=password)

    def validate_email(self, value: str) -> str:
        if CustomUser.objects.filter(email=value).exists():
            raise ValidationError('User with this email already exists')
        return value

    def validate(self, attrs: dict) -> dict:
        if attrs['password1'] != attrs['password2']:
            raise ValidationError({'password2': 'Not equal passwords'})
        try:
            validate_password(password=attrs['password1'])
        except DjangoValidationError as error:
            raise ValidationError({'password1': error.messages})
        return attrs


class CustomUserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs: dict) -> dict:
        user = self.context['request'].user
        if not check_password(attrs['old_password'], user.password):
            raise ValidationError({'old_password': 'Old password not correct'})
        if attrs['password1'] != attrs['password2']:
            raise ValidationError({'password2': 'Not equal passwords'})
        if attrs['password1'] == attrs['old_password']:
            raise ValidationError('New password must be not equal old password')
        try:
            validate_password(password=attrs['password1'])
        except DjangoValidationError as error:
            raise ValidationError({'password1': error.messages})
        return attrs


class CreateResetPasswordCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data: dict) -> ResetUserPasswordCode:
        return ResetUserPasswordCode.objects.create_for_user(user=self.user)

    def validate_email(self, value: str) -> str:
        email = value
        try:
            self.user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise ValidationError('User with this email not found')
        return value


class ResetPasswordCodeSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='users:resetuserpasswordcode-detail')
    activate_reset_password_url = serializers.HyperlinkedIdentityField(
        view_name='users:resetuserpasswordcode-activate-reset-password',
    )
    reset_password_url = serializers.HyperlinkedIdentityField(view_name='users:resetuserpasswordcode-reset-password')

    class Meta:
        model = ResetUserPasswordCode
        fields = ('pk', 'email', 'created', 'expire_date', 'url', 'activate_reset_password_url',
                  'reset_password_url')


class ActivateResetPasswordSerializer(serializers.Serializer):
    reset_password_code = serializers.CharField(max_length=6)


class ResetPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs: dict) -> dict:
        if attrs['password1'] != attrs['password2']:
            raise ValidationError({'password2': 'Not equal passwords'})
        try:
            validate_password(password=attrs['password1'])
        except DjangoValidationError as error:
            raise ValidationError({'password1': error.messages})
        return attrs
