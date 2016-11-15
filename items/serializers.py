from rest_framework import serializers

from items.models import Category, Item, Image, Like


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'name', 'path', 'item')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'user', 'item')


class ItemSerializer(serializers.ModelSerializer):
    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data['price_min'] > data['price_max']:
            raise serializers.ValidationError("Price min is higher than price max")
        return data

    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'price_min', 'price_max', 'creation_date', 'archived', 'owner',
                  'category')
        read_only_fields = ('owner',)
