from rest_framework import serializers

from items.models import Category, Item, Image
from offers.models import Offer


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('id', 'accepted', 'comment', 'status', 'item_given', 'item_received')
