from django.db import models
from django.utils import timezone


class Offer(models.Model):
    item_given = models.ForeignKey("items.Item", related_name='offers_done', on_delete=models.CASCADE)
    item_received = models.ForeignKey("items.Item", related_name='offers_received', on_delete=models.CASCADE)

    accepted = models.BooleanField(default=False)
    answered = models.BooleanField(default=False)
    comment = models.CharField(max_length=1000)
    creation_date = models.DateTimeField("date published", default=timezone.now)

    def __str__(self):
        return self.comment
