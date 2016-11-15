from rest_framework import serializers

from users.models import *


class UserAccountSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    is_active = serializers.BooleanField(write_only=True)
    location = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserProfile
        fields = (
            'username', 'first_name', 'last_name', 'email', 'is_active', 'location'
        )


# TODO to adapt
"""class NoteSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source="user.id", queryset=User.objects.all())

    class Meta:
        model = Note
        fields = ('id', 'user_id', 'text', 'note')"""
