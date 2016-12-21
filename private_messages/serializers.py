from rest_framework import serializers

from private_messages.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('text', 'date', 'user_from', 'user_to')
