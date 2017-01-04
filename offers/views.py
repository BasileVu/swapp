from django.utils import timezone
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from notifications.models import Notification, OfferNotification, AcceptedOfferNotification, RefusedOfferNotification
from offers.models import Offer
from offers.serializers import OfferSerializer, UpdateOfferSerializer


class OfferViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Offer.objects.all()

    def get_serializer_class(self):
        if self.action == "update":
            return UpdateOfferSerializer

        return OfferSerializer

    def check_items(self, item_given, item_received):
        if item_given is not None and self.request.user != item_given.owner:
            raise ValidationError("Item given is not owned by the current user")
        if item_received is not None and self.request.user == item_received.owner:
            raise ValidationError("Item received is already owned by the current user")

        if item_given is not None and item_received is not None:
            if item_given.price_max < item_received.price_min:
                raise ValidationError("Price max of item given is smaller than price min of item received")

    def perform_create(self, serializer):
        item_given = serializer.validated_data.get("item_given", None)
        item_received = serializer.validated_data.get("item_received", None)
        self.check_items(item_given, item_received)
        serializer.save()
