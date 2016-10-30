from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Defines additional non-authentication- related information about the user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_active = models.BooleanField()
    creation_date = models.DateTimeField('date published')

    def __str__(self):
        return self.username


class Note(models.Model):
    """Defines the note that can be attributed to an user after a proposition was made."""
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    note = models.IntegerField(default=0)

    def __str__(self):
        return self.text
