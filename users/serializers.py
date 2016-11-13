from rest_framework import serializers
from users.models import *


class UserProfileActiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('account_active',)


class UserProfileCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('categories',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('categories', 'account_active', 'creation_date')


class NoteSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source="user.id", queryset=User.objects.all())

    class Meta:
        model = Note
        fields = ('id', 'user_id', 'text', 'note')
