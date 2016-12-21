from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Message(models.Model):
    text = models.CharField(max_length=1000)
    date = models.DateTimeField('date published', default=timezone.now)
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_from')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_to')

    def __str__(self):
        return self.text
