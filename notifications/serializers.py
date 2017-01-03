from rest_framework import serializers

from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    content = serializers.CharField(read_only=True)
    date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Notification
        fields = ('id', 'content', 'read', 'date')
