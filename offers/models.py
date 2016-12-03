from django.utils import timezone

from django.db import models


class Offer(models.Model):
    accepted = models.BooleanField()
    status = models.BooleanField()
    comment = models.CharField(max_length=1000)
    creation_date = models.DateTimeField("date published", default=timezone.now)

    item_given = models.ForeignKey("items.Item", related_name='offers_done', on_delete=models.CASCADE)
    item_received = models.ForeignKey("items.Item", related_name='offers_received', on_delete=models.CASCADE)

    def __str__(self):
        return self.comment
