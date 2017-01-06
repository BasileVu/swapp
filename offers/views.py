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
    map(refuse_offer, item.offers_received.filter(~Q(pk=offer_id), answered=False))
    map(delete_offer, item.offers_done.filter(~Q(pk=offer_id), answered=False))


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
                raise ValidationError("There is already an offer with the same item given and received")

        if item_given.traded:
            raise ValidationError("Item given has already been traded")

        if item_received.traded:
            raise ValidationError("Item received has already been traded")

        if item_given.archived:
            raise ValidationError("Item given does not exist")

        if item_received.archived:
            raise ValidationError("Item received does not exist")

        if self.request.user != item_given.owner:
            raise ValidationError("Item given is not owned by the current user")

        if self.request.user == item_received.owner:
            raise ValidationError("Item received is owned by the current user")

        if item_given.price_max < item_received.price_min:
                raise ValidationError("Price max of item given is smaller than price min of item received")

        serializer.save()

    def perform_update(self, serializer):
        if serializer.instance.accepted:
            raise ValidationError("Can't update an accepted offer")

        accepted = serializer.validated_data.get("accepted", None)

        if accepted is not None:
            if serializer.instance.item_given.owner == self.request.user:
                raise ValidationError("Can't accept or refuse own offer")

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
            raise ValidationError("Can't delete offer of another user")

        if instance.accepted:
            raise ValidationError("Can't delete an accepted offer")
        super().perform_destroy(instance)
