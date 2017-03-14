from rest_framework import serializers

from private_messages.models import Message


class MessageSerializer(serializers.ModelSerializer):
    user_from = serializers.PrimaryKeyRelatedField(read_only=True)
    date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Message
        fields = ('user_from', 'user_to', 'text', 'date')
