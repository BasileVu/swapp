from rest_framework import serializers
from rest_framework.fields import IntegerField

from users.models import *


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)
    street = serializers.CharField(write_only=True)
    city = serializers.CharField(write_only=True)
    region = serializers.CharField(write_only=True)
    country = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password_confirmation',
                  'street', 'city', 'region', 'country')


class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class LoginUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)


class LocationSerializer(serializers.ModelSerializer):
    street = serializers.CharField()
    city = serializers.CharField()
    region = serializers.CharField()
    country = serializers.CharField()

    class Meta:
        model = Location
        fields = ('street', 'city', 'region', 'country')


class NoteSerializer(serializers.ModelSerializer):
    note = IntegerField(max_value=5, min_value=0)

    class Meta:
        model = Note
        fields = ('id', 'user', 'offer', 'text', 'note')
        read_only_fields = ('user',)


class NoteUpdateSerializer(serializers.ModelSerializer):
    note = IntegerField(max_value=5, min_value=0)

    class Meta:
        model = Note
        fields = ('text', 'note')
