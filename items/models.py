from django.forms import forms
from django.utils import timezone

from django.db import models
from rest_framework.exceptions import ValidationError


class Item(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=2000)
    price_min = models.IntegerField(default=0)
    price_max = models.IntegerField(default=0)
    creation_date = models.DateTimeField("date published", default=timezone.now)
    archived = models.BooleanField(default=False)
    views = models.IntegerField(default=0)

    owner = models.ForeignKey("users.UserProfile", on_delete=models.CASCADE)
    category = models.ForeignKey("items.Category", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField('Uploaded image', null=True)

    item = models.ForeignKey("items.Item", on_delete=models.CASCADE)

    def __str__(self):
        return self.image.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey("users.UserProfile", on_delete=models.CASCADE)
    item = models.ForeignKey("items.Item", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.user.username
