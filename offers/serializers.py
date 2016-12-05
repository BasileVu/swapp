from rest_framework import serializers

from offers.models import Offer


class OfferSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if 'item_given' in data and self.context['request'].user != data['item_given'].owner:
            raise serializers.ValidationError("Item given is not owned by the current user")
        if 'item_received' in data and self.context['request'].user == data['item_received'].owner:
            raise serializers.ValidationError("Item received is already owned by the current user")
        return data

    class Meta:
        model = Offer
        fields = ('id', 'accepted', 'comment', 'status', 'item_given', 'item_received')


class OfferItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('id', 'accepted', 'item_given')
