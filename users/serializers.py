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


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)


class LocationSerializer(serializers.ModelSerializer):
    street = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    region = serializers.CharField(required=True)
    country = serializers.CharField(required=True)

    class Meta:
        model = Location
        fields = ('street', 'city', 'region', 'country')


class NoteSerializer(serializers.ModelSerializer):
    """def validate(self, data):
        if 'item_given' in data and self.context['request'].user != data['item_given'].owner:
            raise serializers.ValidationError("Item given is not owned by the current user")
        if 'item_received' in data and self.context['request'].user == data['item_received'].owner:
            raise serializers.ValidationError("Item received is already owned by the current user")
        return data"""

    class Meta:
        model = Note
        fields = ('id', 'user', 'offer', 'text', 'note')

