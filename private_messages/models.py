from django.db import models


class Message(models.Model):
    text = models.CharField(max_length=1000)
    date = models.DateTimeField('date published')
    user = models.ForeignKey("users.UserProfile", on_delete=models.CASCADE)
    item = models.ForeignKey("items.Item", on_delete=models.CASCADE)

    def __str__(self):
        return self.text
