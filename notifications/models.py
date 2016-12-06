from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from comments.models import Comment
from offers.models import Offer
from users.models import Note


class Notification(models.Model):
    content = models.CharField(max_length=100)
    read = models.BooleanField()
    date = models.DateTimeField('date published')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class MessageNotification(models.Model):
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)


class CommentNotification(models.Model):
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


class OfferNotification(models.Model):
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)


class NewOfferNotification(models.Model):
    offer_notification = models.OneToOneField(OfferNotification, on_delete=models.CASCADE)


@receiver(post_save, sender=Offer)
def new_offer_notification(sender, instance, signal, created, **kwargs):
    """
    Handler to create a notification when an offer is created.
    """
    if created:
        notification = Notification.objects.create(content="New offer for item: " + instance.item_receveid.name,
                                                   read=False, date=timezone.now(), user=instance.item_receveid.owner)
        offer_notification = OfferNotification.objects.create(notification=notification, offer=instance)
        NewOfferNotification.objects.create(offer_notification=offer_notification)


class AcceptedOfferNotification(models.Model):
    offer_notification = models.OneToOneField(OfferNotification, on_delete=models.CASCADE)


class RefusedOfferNotification(models.Model):
    offer_notification = models.OneToOneField(OfferNotification, on_delete=models.CASCADE)
