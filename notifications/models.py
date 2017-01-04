from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from comments.models import Comment
from offers.models import Offer
from private_messages.models import Message
from users.models import Note


class Notification(models.Model):
    content = models.CharField(max_length=100)
    read = models.BooleanField(default=False)
    date = models.DateTimeField('date published', default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class MessageNotification(models.Model):
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE)
    message = models.OneToOneField(Message, on_delete=models.CASCADE)


@receiver(post_save, sender=Message)
def new_message_notification(sender, instance, signal, created, **kwargs):
    """
    Handler to create a notification when a message is created.
    """
    if created:
        notification = Notification.objects.create(content="New private message", user=instance.user_to)
        MessageNotification.objects.create(notification=notification, message=instance)


class NoteNotification(models.Model):
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE)
    note = models.OneToOneField(Note, on_delete=models.CASCADE)


@receiver(post_save, sender=Note)
def new_note_notification(sender, instance, signal, created, **kwargs):
    """
    Handler to create a notification when a note is given (created).
    """
    if created:
        notification = Notification.objects.create(content="New note %d with text: %s" % (instance.note, instance.text),
                                                   user=instance.offer.item_received.owner)
        NoteNotification.objects.create(notification=notification, note=instance)


class CommentNotification(models.Model):
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE)
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE)


@receiver(post_save, sender=Comment)
def new_comment_notification(sender, instance, signal, created, **kwargs):
    """
    Handler to create a notification when a comment is created.
    """
    if created:
        notification = Notification.objects.create(content="%s has commented your item: %s" %
                                                           (instance.user.username, instance.item.name),
                                                   user=instance.item.owner)
        CommentNotification.objects.create(notification=notification, comment=instance)


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
        notification = Notification.objects.create(content="New offer for item: %s" % instance.item_received.name,
                                                   user=instance.item_received.owner)
        offer_notification = OfferNotification.objects.create(notification=notification, offer=instance)
        NewOfferNotification.objects.create(offer_notification=offer_notification)


class AcceptedOfferNotification(models.Model):
    offer_notification = models.OneToOneField(OfferNotification, on_delete=models.CASCADE)


class RefusedOfferNotification(models.Model):
    offer_notification = models.OneToOneField(OfferNotification, on_delete=models.CASCADE)
