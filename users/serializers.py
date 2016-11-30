from rest_framework import serializers

from users.models import *


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class LoginUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password')


# TODO to adapt
"""class NoteSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source="user.id", queryset=User.objects.all())

    class Meta:
        model = Note
        fields = ('id', 'user_id', 'text', 'note')"""


class LocationSerializer(serializers.ModelSerializer):
    street = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    region = serializers.CharField(required=True)
    country = serializers.CharField(required=True)

    class Meta:
        model = Location
        fields = ('street', 'city', 'region', 'country')
