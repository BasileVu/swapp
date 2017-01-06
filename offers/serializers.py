from rest_framework import serializers

from offers.models import Offer


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ("id", "accepted", "comment", "answered", "item_given", "item_received")


class UpdateOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ("accepted", "comment", "answered")
