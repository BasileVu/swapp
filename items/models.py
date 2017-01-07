from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone


class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=2000)
    price_min = models.IntegerField(default=0)
    price_max = models.IntegerField(default=0)
    creation_date = models.DateTimeField("date published", default=timezone.now)
    views = models.IntegerField(default=0)
    traded = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey("items.Category", on_delete=models.CASCADE)
    delivery_methods = models.ManyToManyField("items.DeliveryMethod")

    def __str__(self):
        return self.name


class DeliveryMethod(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class KeyInfo(models.Model):
    key = models.CharField(max_length=30)
    info = models.CharField(max_length=30)

    item = models.ForeignKey(Item, on_delete=models.CASCADE)


class Image(models.Model):
    image = models.ImageField("Uploaded image", null=True)

    item = models.ForeignKey("items.Item", on_delete=models.CASCADE)

    def __str__(self):
        return self.image.name


@receiver(pre_delete, sender=Image)
def image_delete(sender, instance, **kwargs):
    """
    Delete the file associated with the image field.
    """

    # Pass false so ImageField doesn't save the model
    instance.image.delete(False)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey("items.Item", on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username
