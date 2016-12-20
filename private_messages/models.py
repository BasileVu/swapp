from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Message(models.Model):
    text = models.CharField(max_length=1000)
    date = models.DateTimeField('date published', default=timezone.now)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    item = models.ForeignKey("items.Item", on_delete=models.CASCADE)

    def __str__(self):
        return self.text
