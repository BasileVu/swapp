from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class UserProfile(models.Model):
    """Defines additional non-authentication- related information about the user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_active = models.BooleanField()
    # On ne peut pas plutôt utiliser directement le champ date_joined de l'User de Django ?
    # Plutôt mettre alors une date de dernière modification des infos du compte non ?
    # Par contre trouver un moyen de faire un trigger propre sur une modification.
    # creation_date = models.DateTimeField("date published")
    last_modification_date = models.DateTimeField("date last modification")

    categories = models.ManyToManyField("items.Category")

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, signal, created, **kwargs):
    """Handler to create user profile when an user is created"""
    if created:
        # UserProfile(user=instance, account_active=False, creation_date=timezone.now()).save()
        UserProfile(user=instance, account_active=False, last_modification_date=timezone.now()).save()


class Note(models.Model):
    """Defines the note that can be attributed to an user after a proposition was made."""
    user = models.ForeignKey("users.UserProfile", on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    note = models.IntegerField(default=0)

    def __str__(self):
        return self.text
