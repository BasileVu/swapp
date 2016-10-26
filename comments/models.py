from django.db import models


class Comment(models.Model):
    content = models.CharField(max_length=1000)
    date = models.DateTimeField('date published')

    def __str__(self):
        return self.content
