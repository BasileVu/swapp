from django.db import models


class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    account_active = models.BooleanField()
    creation_date = models.DateTimeField('date published')

    def __str__(self):
        return self.username

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    note = models.IntegerField(default=0)

    def __str__(self):
        return self.text
