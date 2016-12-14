from django.utils import timezone
from rest_framework import viewsets

from notifications.models import Notification, OfferNotification, AcceptedOfferNotification, RefusedOfferNotification
from offers.models import Offer
from offers.serializers import OfferSerializer


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def perform_update(self, serializer):
        offer = serializer.save()

        if offer.accepted:
            # create notification for accepted offer
            notification = Notification.objects.create(content="Offer accepted for item: " + offer.item_received.name,
                                                       read=False, date=timezone.now(), user=offer.item_received.owner)
            offer_notification = OfferNotification.objects.create(notification=notification, offer=offer)
            AcceptedOfferNotification.objects.create(offer_notification=offer_notification)
        else:
            # create notification for refused offer
            notification = Notification.objects.create(content="Offer refused for item: " + offer.item_received.name,
                                                       read=False, date=timezone.now(), user=offer.item_received.owner)
            offer_notification = OfferNotification.objects.create(notification=notification, offer=offer)
            RefusedOfferNotification.objects.create(offer_notification=offer_notification)
