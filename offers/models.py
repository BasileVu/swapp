from django.db import models


class Offer(models.Model):
    accepted = models.BooleanField()
    status = models.BooleanField()
    comment = models.CharField(max_length=1000)
    date = models.DateTimeField('date published')

    def __str__(self):
        return self.comment
