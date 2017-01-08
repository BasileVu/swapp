from django.db.models import Q
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from offers.models import Offer
from offers.serializers import CreateOfferSerializer, RetrieveOfferSerializer, UpdateOfferSerializer


def delete_offer(offer):
    offer.delete()


def refuse_offer(offer):
    offer.answered = True
    offer.accepted = False
    offer.save()


def refuse_and_delete_pending_offers(item, offer_id):
    """
    Refuses received pending received offers and deletes done pending offers.

    :param item: the item on which to refuse and delete offers.
    :param offer_id: the id of the offer to exclude when refusing and deleting.
    """
    for o in item.offers_received.filter(~Q(pk=offer_id), answered=False):
        refuse_offer(o)

    for o in item.offers_done.filter(~Q(pk=offer_id), answered=False):
        delete_offer(o)


class OfferViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):

    queryset = Offer.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "create":
            return CreateOfferSerializer
        if self.action in ["update", "partial_update"]:
            return UpdateOfferSerializer
        return RetrieveOfferSerializer

    def perform_create(self, serializer):
        item_given = serializer.validated_data["item_given"]
        item_received = serializer.validated_data["item_received"]

        for o in item_given.offers_done.filter(answered=False):
            if item_received == o.item_received:
                raise ValidationError("You have already created an offer with the same item for the wanted item")

        for o in item_received.offers_done.filter(answered=False):
            if item_given == o.item_received:
                raise ValidationError("There is already an offer for your item with the wanted item. Please accept it")

        if item_given.traded:
            raise ValidationError("You can't create an offer with an item that has been traded")

        if item_received.traded:
            raise ValidationError("You can't create an offer for an item that has been traded")

        if item_given.archived:
            raise ValidationError("The item traded does not exist")

        if item_received.archived:
            raise ValidationError("The item wanted does not exist")

        if self.request.user != item_given.owner:
            raise ValidationError("You can't trade another person's item")

        if self.request.user == item_received.owner:
            raise ValidationError("You can't traded for your own item")

        if item_given.price_max < item_received.price_min:
                raise ValidationError("Price max of your item is smaller than price min of the wanted item")

        serializer.save()

    def perform_update(self, serializer):
        if serializer.instance.accepted:
            raise ValidationError("You can't update an accepted offer")

        accepted = serializer.validated_data.get("accepted", None)

        if accepted is not None:
            if serializer.instance.item_given.owner == self.request.user:
                raise ValidationError("You can't accept or refuse your own offer")

            serializer.validated_data["answered"] = True

            if accepted:
                offer = serializer.instance

                offer.item_given.traded = True
                offer.item_given.save()
                offer.item_received.traded = True
                offer.item_received.save()

                refuse_and_delete_pending_offers(offer.item_given, offer.id)
                refuse_and_delete_pending_offers(offer.item_received, offer.id)

        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.item_given.owner:
            raise ValidationError("You can't delete offer of another user")

        if instance.accepted:
            raise ValidationError("You can't delete an accepted offer")
        super().perform_destroy(instance)
