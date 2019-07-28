from rest_framework import serializers

from utils.validators import text_validator, string_with_space_validator, mobile_number_validator
from . import models


class SignUpSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50, validators=[text_validator, string_with_space_validator])
    email = serializers.EmailField(max_length=50)
    password = serializers.CharField(max_length=150)
    mobile = serializers.CharField(max_length=15, validators=[mobile_number_validator])

    class Meta:
        model = models.User
        fields = ('name', 'email', 'mobile', 'password')


class SignInSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50)
    password = serializers.CharField(max_length=150)

    class Meta:
        model = models.User
        fields = ('email', 'password')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'id', 'name', 'email', 'mobile', 'is_mobile_verified', 'is_email_verified', 'city', 'state', 'country',)
