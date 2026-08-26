from turtle import st

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken , TokenError
from rest_framework import status
from rest_framework.response import Response
from .models import blog

class blogserializer(serializers.ModelSerializer):
    class Meta:
        model = blog
        fields = '__all__' 

class Registerationserializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class refreshserialier(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self,attrs):
        refresh_token = attrs.get("refresh")

        try:
            token = RefreshToken(refresh_token)

            attrs["access"] = str(token.access_token)

        except TokenError:
            raise serializers.ValidationError(
                {
                    "ERROR":"your refresh token is invalid"
                },status=status.HTTP_401_UNAUTHORIZED
            )
        return attrs
