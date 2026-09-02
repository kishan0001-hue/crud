from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken , TokenError
from rest_framework import status
from .models import blog

class blogserializer(serializers.ModelSerializer):
    class Meta:
        model = blog
        fields = [
            'id',
            'author',
            'name',
            'topic',
            'discription',
            'image',
            'created_at',
            'updated_at',
        ]

        read_only_field = [
            'id',
            'author',
            'created_at',
            'updatde_at',
        ]

class Registerationserializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only = True
    )

    class Meta:
        model= User
        fields = [
            'username',
            'email',
            'password',
        ]

    def create(self, validated_data):
        user =  User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email',''),
            password=validated_data['password']
        )

        return user

class VerifyOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()
    otp = serializers.CharField(min_length=6,max_length=6)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)

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
