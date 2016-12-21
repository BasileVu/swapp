from rest_framework import viewsets
from private_messages.models import Message
from private_messages.serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
