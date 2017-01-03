from rest_framework import serializers

from items.models import Category, Item, Image, Like
from swapp.gmaps_api_utils import MAX_RADIUS


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class CreateImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
    item = serializers.IntegerField(required=False)
    user = serializers.IntegerField(required=False)

    class Meta:
        field = ('image', 'item', 'user')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image', 'item')


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'user', 'item')


# FIXME : DELETE ImageItemSerializer and LikeItemSerializer


class ImageItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image')


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'price_min', 'price_max', 'category')


class AggregatedItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    image_urls = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    offers_received = serializers.SerializerMethodField()
    owner_username = serializers.SerializerMethodField()

    def get_image_urls(self, obj):
        return [i.image.url for i in obj.image_set.all()]

    def get_likes(self, obj):
        return obj.like_set.count()

    def get_comments(self, obj):
        return obj.comment_set.count()

    def get_offers_received(self, obj):
        return obj.offers_received.count()

    def get_owner_username(self, obj):
        return obj.owner.username

    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'price_min', 'price_max', 'creation_date', 'owner_username', 'category',
                  'views', 'image_urls', 'likes', 'comments', 'offers_received')
        read_only_fields = ('owner',)


class SearchItemsSerializer(serializers.Serializer):
    q = serializers.CharField(default="")
    category = serializers.CharField(default=None)
    lat = serializers.FloatField(default=None)
    lon = serializers.FloatField(default=None)
    radius = serializers.FloatField(default=MAX_RADIUS)
    price_min = serializers.FloatField(default=0)
    price_max = serializers.FloatField(default=None)
    order_by = serializers.CharField(default=None)
    limit = serializers.IntegerField(default=None)
    page = serializers.IntegerField(default=None)
