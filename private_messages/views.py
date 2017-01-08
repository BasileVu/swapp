from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from private_messages.models import Message
from private_messages.serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user_from=self.request.user)
