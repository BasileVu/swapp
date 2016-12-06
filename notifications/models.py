from django.db import models


class Notification(models.Model):
    content = models.CharField(max_length=100)
    read = models.BooleanField()
    date = models.DateTimeField('date published')

    def __str__(self):
        return self.content


class MessageNotification(models.Model):
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE)


class CommentNotification(models.Model):
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE)


class OfferNotification(models.Model):
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE)


class NewOfferNotification(models.Model):
    offer_notification = models.OneToOneField(OfferNotification, on_delete=models.CASCADE)


class AcceptedOfferNotification(models.Model):
    offer_notification = models.OneToOneField(OfferNotification, on_delete=models.CASCADE)


class RefusedOfferNotification(models.Model):
    offer_notification = models.OneToOneField(OfferNotification, on_delete=models.CASCADE)
