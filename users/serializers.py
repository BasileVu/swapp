from rest_framework import serializers
from users.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source="user.id", queryset=User.objects.all())
    username = serializers.PrimaryKeyRelatedField(source="user.username", queryset=User.objects.all())
    email = serializers.PrimaryKeyRelatedField(source="user.email", queryset=User.objects.all())

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'categories', 'account_active', 'creation_date')


class NoteSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source="user.id", queryset=User.objects.all())

    class Meta:
        model = Note
        fields = ('id', 'user_id', 'text', 'note')
