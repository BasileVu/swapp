from django.db import models


class Message(models.Model):
    text = models.CharField(max_length=100)
    date = models.DateTimeField('date published')

    def __str__(self):
        return self.text
