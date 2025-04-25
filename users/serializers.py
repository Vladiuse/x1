from rest_framework import serializers

class CustomUserLoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField()