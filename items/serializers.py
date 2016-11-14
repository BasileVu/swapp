from django.contrib.auth.models import User
from rest_framework import serializers

from items.models import Category, Item, Image


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
        model = Category
        fields = ('id', 'user', 'item')


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'price_min', 'price_max', 'creation_date', 'archived', 'owner',
                  'category')
