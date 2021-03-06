from django.contrib.auth.models import User
from django.db.models import F, FloatField, IntegerField
from django.db.models import Func
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from comments.serializers import CommentSerializer
from items.serializers import *
from users.models import Consultation


def check_prices(price_min, price_max):
    if price_min is not None and price_min < 0:
        raise ValidationError("Price min is negative")

    if price_max is not None and price_max < 0:
        raise ValidationError("Price max is negative")

    if price_min is not None and price_max is not None and price_min > price_max:
        raise ValidationError("Price min is higher than price max")


def filter_items(data, user):
    q = data["q"]
    category = data["category"]
    price_min = data["price_min"]
    price_max = data["price_max"]
    lat = data["lat"]
    lon = data["lon"]
    radius = data["radius"]
    order_by = data["order_by"]

    queryset = Item.objects.filter(
        Q(name__icontains=q) | Q(description__icontains=q),
        price_min__gte=price_min, traded=False, archived=False
    )

    if user.is_authenticated:
        queryset = queryset.filter(~Q(owner=user))

    if category is not None:
        queryset = queryset.filter(category__name=category)

    if price_max is not None:
        queryset = queryset.filter(price_max__lte=price_max)

    if user.is_authenticated and (lat is None or lon is None):
        lat = user.coordinates.latitude
        lon = user.coordinates.longitude

    if lat is not None and lon is not None:
        # add "distance" field to each object
        queryset = queryset.annotate(
            distance=Func(lat, lon, F("owner__coordinates__latitude"), F("owner__coordinates__longitude"),
                          function="compute_distance", output_field=FloatField())
        )

        queryset = queryset.filter(distance__lte=radius)

    if order_by is None:
        queryset = queryset.order_by("creation_date")
    else:
        strings_order_by = {
            "name": "name",
            "category": "category__name",
            "price_min": "price_min",
            "price_max": "-price_max",
            "range": "distance",
            "date": "creation_date"
        }
        queryset = queryset.order_by(strings_order_by[order_by])

    return queryset


def last_similar_points(item, items):
    n_cat_similar = 0
    for i in items:
        if item.category == i.category:
            n_cat_similar += 1
    if n_cat_similar > 9:
        return 11
    if n_cat_similar > 6:
        return 9
    if n_cat_similar > 5:
        return 3
    if n_cat_similar > 1:
        return 2
    return 0


def mean_user_notes(user):
    note_avg = user.userprofile.note_avg
    return 5 if note_avg is None else note_avg


def note_mean_points(mean_user, mean_all_users):
    if mean_user > mean_all_users:
        return 5
    if mean_user == mean_all_users:
        return 3
    return 0


def num_comments_points(n_comments, mean_comments_number):
    if n_comments > mean_comments_number:
        return 6
    elif n_comments == mean_comments_number:
        return 3
    return 0


def num_offers_points(n_offers, mean_offer_number):
    if n_offers > mean_offer_number:
        return 5
    return 0


def build_item_suggestions(user):
    queryset = Item.objects.filter(traded=False, archived=False)

    if user.is_authenticated:
        lon = user.coordinates.longitude
        lat = user.coordinates.latitude
        queryset = queryset.filter(~Q(owner=user))
    else:
        lon = 0
        lat = 0

    queryset = queryset.annotate(
        distance=Func(
            lat, lon, F("owner__coordinates__latitude"), F("owner__coordinates__longitude"),
            function="compute_distance", output_field=FloatField()
        )
    ).annotate(
        points=Func(
            F("distance"), function="distance_points", output_field=IntegerField()
        )
    )

    items = list()

    all_users = User.objects.all()
    n_users = len(all_users)
    n_items = len(queryset)

    if n_users > 0:
        mean_all_users = sum(mean_user_notes(user) for user in all_users) / n_users

    sum_comments = 0
    sum_offers = 0

    for i in queryset:
        sum_comments += i.comment_set.count()
        sum_offers += i.offers_received.count()

    if n_items > 0:
        mean_comments_number = sum_comments / n_items
        mean_offers_number = sum_offers / n_items

    if user.is_authenticated:
        recent_items_liked = [like.item for like in user.like_set.order_by("date")[:10]]
        recent_items_visited = [consultation.item for consultation in user.consultation_set.order_by("date")[:10]]

    for item in queryset:
        item.points *= 20

        if user.is_authenticated:
            if item.category in user.userprofile.categories.all():
                item.points += 15

            item.points += last_similar_points(item, recent_items_liked) * 11
            item.points += last_similar_points(item, recent_items_visited) * 7

        item.points += item.like_set.count() * 6
        item.points += note_mean_points(mean_user_notes(item.owner), mean_all_users) * 5
        item.points += num_comments_points(item.comment_set.count(), mean_comments_number) * 2
        item.points += num_offers_points(item.offers_received.count(), mean_offers_number)

        items.append(item)

    items.sort(key=lambda i: (-i.points, i.distance))
    return items


class ItemViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return DetailedItemSerializer
        return ItemSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = Item.objects.all()
        item = get_object_or_404(queryset, pk=pk)

        if request.user.is_authenticated:
            Consultation.objects.create(user=self.request.user, item=item)

        item.views += 1
        item.save()

        serializer = DetailedItemSerializer(item, context={"request": self.request})
        return Response(serializer.data)

    @detail_route(methods=["GET"])
    def comments(self, request, pk=None):
        return Response(CommentSerializer(Item.objects.get(pk=pk).comment_set.order_by("-date"), many=True).data)

    @detail_route(methods=["POST"])
    def archive(self, request, pk=None):
        item = Item.objects.get(pk=pk)

        if item.offers_received.filter(answered=False).count() > 0 or item.offers_done.filter(answered=False).count() > 0:
            raise ValidationError("You can't archive this item since it has pending offers")

        item.archived = True
        item.save()

        return Response()

    @detail_route(methods=["POST"])
    def restore(self, request, pk=None):
        item = Item.objects.get(pk=pk)
        item.archived = False
        item.save()

        return Response()

    @detail_route(methods=["POST"])
    def images(self, request, pk=None):
        serializer = CreateImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item = get_object_or_404(Item, pk=pk)
        i = Image.objects.create(image=serializer.validated_data["image"], item=item)

        return Response(status=status.HTTP_201_CREATED, data=ImageSerializer(i).data, headers={"Location": i.image.url})

    def list(self, request, *args, **kwargs):
        serializer = SearchItemsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        user = request.user

        if len(request.query_params) == 0:
            items = build_item_suggestions(user)
            return Response(DetailedItemSerializer(items, many=True, context={"request": self.request}).data)
        else:
            queryset = filter_items(serializer.validated_data, user)
            return Response(DetailedItemSerializer(queryset, many=True, context={"request": self.request}).data)

    def perform_create(self, serializer):
        price_min = serializer.validated_data.get("price_min", None)
        price_max = serializer.validated_data.get("price_max", None)

        check_prices(price_min, price_max)
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        item = serializer.instance

        if item.traded:
            raise ValidationError("Can't update a traded item")

        if item.archived:
            raise ValidationError("Can't update an archived item")

        offers_received_pending = item.offers_received.filter(answered=False)
        offers_done_pending = item.offers_done.filter(answered=False)

        if offers_done_pending.count() > 0 or offers_received_pending.count() > 0:
            raise ValidationError("Can't update an item with pending offers")

        price_min = serializer.validated_data.get("price_min", serializer.instance.price_min)
        price_max = serializer.validated_data.get("price_max", serializer.instance.price_max)
        check_prices(price_min, price_max)

        serializer.save()


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DeliveryMethodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DeliveryMethod.objects.all()
    serializer_class = DeliveryMethodSerializer


class ImageViewSet(mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Image.objects.all()
    permission_classes = (IsAuthenticated,)


class LikeViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user).order_by("-date")

    def perform_create(self, serializer):
        item = serializer.validated_data["item"]
        user = self.request.user

        if item in user.item_set.all():
            raise ValidationError("You cannot like your own item")

        for like in self.request.user.like_set.all():
            if like.item == item:
                raise ValidationError("An item cannot be liked twice")

        serializer.save(user=user)
