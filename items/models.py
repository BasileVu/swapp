from django.utils import timezone

from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=2000)
    price_min = models.IntegerField(default=0)
    price_max = models.IntegerField(default=0)
    creation_date = models.DateTimeField("date published", default=timezone.now)
    archived = models.BooleanField(default=False)

    owner = models.ForeignKey("users.UserProfile", on_delete=models.CASCADE)
    category = models.ForeignKey("items.Category", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=200)

    item = models.ForeignKey("items.Item", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey("users.UserProfile", on_delete=models.CASCADE)
    item = models.ForeignKey("items.Item", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
