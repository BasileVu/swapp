from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from swapp.gmaps_api_utils import get_coordinates


class UserProfile(models.Model):
    """
    Defines additional non-authentication-related information about the user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_modification_date = models.DateTimeField(auto_now=True)

    categories = models.ManyToManyField("items.Category")

    def __str__(self):
        return "User profile of " + self.user.username


class Location(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    country = models.CharField(max_length=50)


class Coordinates(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True, default=0)
    longitude = models.FloatField(null=True, blank=True, default=0)


@receiver(post_save, sender=User)
def create_user_related(sender, instance, signal, created, **kwargs):
    """
    Handler to create user-related tables when user created: user profile, location and coordinates.
    """
    if created:
        UserProfile.objects.create(user=instance, last_modification_date=timezone.now())
        Location.objects.create(user=instance)
        Coordinates.objects.create(user=instance)
    else:
        # When we make a modification on the User (fields), we change the field "last_modification_date"
        # with the new datetime.
        instance.userprofile.save()


class Note(models.Model):
    """
    Defines the note that can be attributed to an user after a proposition was made.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    note = models.IntegerField(default=0)

    def __str__(self):
        return self.text
