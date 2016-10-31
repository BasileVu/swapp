from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=2000)
    price_min = models.IntegerField(default=0)
    price_max = models.IntegerField(default=0)
    creation_date = models.DateTimeField('date published')
    archived = models.BooleanField()

    def __str__(self):
        return self.name


class Media(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Image(Media):
    path = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
