from django.db import models


class Notification(models.Model):
    content = models.CharField(max_length=100)
    read = models.BooleanField()
    date = models.DateTimeField('date published')

    def __str__(self):
        return self.content