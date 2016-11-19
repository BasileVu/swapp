from rest_framework import serializers

from items.models import Category, Item, Image, Like


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image', 'item')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'user', 'item')

class ImageItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image')

class LikeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'user')


class ItemSerializer(serializers.ModelSerializer):
    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if 'price_min' in data and 'price_max' in data and data['price_min'] > data['price_max']:
            raise serializers.ValidationError("Price min is higher than price max")
        return data

    category = CategorySerializer(many=False)
    image_set = ImageItemSerializer(many=True)
    like_set = LikeItemSerializer(many=True)

    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'price_min', 'price_max', 'creation_date', 'archived', 'owner',
                  'category', 'image_set', 'like_set')
        read_only_fields = ('owner',)
