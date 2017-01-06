from rest_framework import serializers

from offers.models import Offer


class CreateOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ("id", "comment", "item_given", "item_received")


class RetrieveOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ("id", "accepted", "comment", "answered", "item_given", "item_received")


class UpdateOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ("accepted", "comment", "answered")
