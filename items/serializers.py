from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from items.models import Category, Item, Image, Like, KeyInfo, DeliveryMethod
from swapp.gmaps_api_utils import MAX_RADIUS


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class DeliveryMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryMethod
        fields = ("id", "name")


class InterestedByCategorySerializer(serializers.Serializer):
    interested_by = serializers.ListField(
        child=serializers.IntegerField()
    )

    class Meta:
        fields = ("interested_by",)


class CreateImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
    item = serializers.IntegerField(required=False)
    user = serializers.IntegerField(required=False)

    class Meta:
        fields = ("image", "item", "user")


class ImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return obj.image.url

    class Meta:
        model = Image
        fields = ("id", "url")


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
    delivery_methods = serializers.PrimaryKeyRelatedField(many=True, queryset=DeliveryMethod.objects.all())

    def create(self, validated_data):
        key_info_set = validated_data.pop("keyinfo_set")
        delivery_methods = validated_data.pop("delivery_methods")

        if len(delivery_methods) == 0:
            raise ValidationError("A least one delivery method should be specified")

        item = Item.objects.create(**validated_data)

        for key_info in key_info_set:
            item.keyinfo_set.add(KeyInfo.objects.create(key=key_info["key"], info=key_info["info"], item=item))

        for delivery_method in delivery_methods:
            item.delivery_methods.add(DeliveryMethod.objects.get(pk=delivery_method.id))

        return item

    def update(self, instance, validated_data):
        if validated_data.get("keyinfo_set", None) is not None:
            keyinfo_set = validated_data.pop("keyinfo_set")
            instance.keyinfo_set.all().delete()

            for key_info in keyinfo_set:
                instance.keyinfo_set.add(KeyInfo.objects.create(key=key_info["key"], info=key_info["info"],
                                                                item=instance))

        if validated_data.get("delivery_methods", None) is not None:
            delivery_methods = validated_data.pop("delivery_methods")

            if len(delivery_methods) == 0:
                raise ValidationError("A least one delivery method should be specified")

            instance.delivery_methods.clear()

            for delivery_method in delivery_methods:
                instance.delivery_methods.add(DeliveryMethod.objects.get(pk=delivery_method.id))

        return super().update(instance, validated_data)

    class Meta:
        model = Item
        fields = ("id", "name", "description", "price_min", "price_max", "category", "keyinfo_set", "delivery_methods")


class InventoryItemSerializer(serializers.ModelSerializer):
    image_id = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    def get_image_id(self, obj):
        return obj.image_set.first().id if obj.image_set.count() > 0 else None

    def get_image_url(self, obj):
        return obj.image_set.first().image.url if obj.image_set.count() > 0 else None

    class Meta:
        model = Item
        fields = ("id", "name", "image_id", "image_url", "archived")


class DetailedItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    keyinfo_set = KeyInfoSerializer(many=True)
    delivery_methods = DeliveryMethodSerializer(many=True)
    images = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    offers_received = serializers.SerializerMethodField()
    owner_username = serializers.SerializerMethodField()
    similar = serializers.SerializerMethodField()
    owner_picture_url = serializers.SerializerMethodField()
    owner_location = serializers.SerializerMethodField()

    def get_images(self, obj):
        return ImageSerializer(obj.image_set.all(), many=True).data

    def get_likes(self, obj):
        return obj.like_set.count()

    def get_comments(self, obj):
        return obj.comment_set.count()

    def get_offers_received(self, obj):
        return obj.offers_received.count()

    def get_owner_username(self, obj):
        return obj.owner.username

    def get_similar(self, obj):
        return InventoryItemSerializer(Item.objects.filter(~Q(pk=obj.id), category=obj.category), many=True).data

    def get_owner_picture_url(self, obj):
        return obj.owner.userprofile.image.url if obj.owner.userprofile.image.name != "" else None

    def get_owner_location(self, obj):
        location = obj.owner.location
        return "%s, %s" % (location.city, location.country)

    class Meta:
        model = Item
        fields = ("id", "name", "description", "price_min", "price_max", "creation_date", "owner_username", "category",
                  "views", "images", "likes", "comments", "offers_received", "keyinfo_set", "delivery_methods",
                  "similar", "owner_picture_url", "owner_location", "traded", "archived")


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
