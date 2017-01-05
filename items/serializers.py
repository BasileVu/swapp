from rest_framework import serializers

from items.models import Category, Item, Image, Like, KeyInfo
from swapp.gmaps_api_utils import MAX_RADIUS


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class CreateImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
    item = serializers.IntegerField(required=False)
    user = serializers.IntegerField(required=False)

    class Meta:
        field = ("image", "item", "user")


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("id", "image", "item")


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Like
        fields = ("id", "user", "item", "date")


class KeyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyInfo
        fields = ("key", "info")


class ItemSerializer(serializers.ModelSerializer):
    keyinfo_set = KeyInfoSerializer(many=True)

    def create(self, validated_data):
        key_info_set = validated_data.pop("keyinfo_set")
        item = Item.objects.create(**validated_data)

        for key_info in key_info_set:
            item.keyinfo_set.add(KeyInfo.objects.create(key=key_info["key"], info=key_info["info"], item=item))

        return item

    def update(self, instance, validated_data):
        if validated_data.get("keyinfo_set", None) is not None:
            keyinfo_set = validated_data.pop("keyinfo_set")
            instance.keyinfo_set.all().delete()

            for key_info in keyinfo_set:
                instance.keyinfo_set.add(KeyInfo.objects.create(key=key_info["key"], info=key_info["info"],
                                                                item=instance))

        return super().update(instance, validated_data)

    class Meta:
        model = Item
        fields = ("id", "name", "description", "price_min", "price_max", "category", "keyinfo_set")


class InventoryItemSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        return obj.image_set.first().image.url if obj.image_set.count() > 0 else None

    class Meta:
        model = Item
        fields = ("id", "name", "image_url")


class DetailedItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    keyinfo_set = KeyInfoSerializer(many=True)
    image_urls = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    offers_received = serializers.SerializerMethodField()
    owner_username = serializers.SerializerMethodField()
    similar = serializers.SerializerMethodField()
    owner_picture_url = serializers.SerializerMethodField()
    owner_location = serializers.SerializerMethodField()

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

    def get_similar(self, obj):
        return InventoryItemSerializer(Item.objects.filter(category=obj.category).exclude(pk=obj.id), many=True).data
    
    def get_owner_picture_url(self, obj):
        return obj.owner.userprofile.image.url if obj.owner.userprofile.image.name != "" > 0 else None

    def get_owner_location(self, obj):
        location = obj.owner.location
        return "%s, %s" % (location.city, location.country)

    class Meta:
        model = Item
        fields = ("id", "name", "description", "price_min", "price_max", "creation_date", "owner_username", "category",
                  "views", "image_urls", "likes", "comments", "offers_received", "keyinfo_set", "similar",
                  "owner_picture_url", "owner_location")


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
