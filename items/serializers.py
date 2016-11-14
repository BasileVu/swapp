from django.contrib.auth.models import User
from rest_framework import serializers

from items.models import Category, Item


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'price_min', 'price_max', 'creation_date', 'archived', 'owner',
                  'category')
