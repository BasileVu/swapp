from django.contrib.auth.models import User
from django.db.models import F, FloatField, Avg, IntegerField
from django.db.models import Func
from django.db.models import Q
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from comments.models import Comment
from items.serializers import *
from users.models import Consultation


def check_prices(price_min, price_max):
    if price_min is not None and price_min < 0:
        raise ValidationError("Price min is negative")

    if price_max is not None and price_max < 0:
        raise ValidationError("Price max is negative")

    if price_min is not None and price_max is not None and price_min > price_max:
        raise ValidationError("Price min is higher than price max")


def filter_items(data):
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
        price_min__gte=price_min, archived=False
    )

    if category is not None:
        queryset = queryset.filter(category__name=category)

    if price_max is not None:
        queryset = queryset.filter(price_max__lte=price_max)

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


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return AggregatedItemSerializer
        return ItemSerializer

    def retrieve(self, request, pk=None):
        queryset = Item.objects.all()
        item = get_object_or_404(queryset, pk=pk)

        if request.user.is_authenticated():
            Consultation.objects.create(user=self.request.user, item=item)

        item.views += 1
        item.save()

        serializer = AggregatedItemSerializer(item)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        serializer = SearchItemsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        user = request.user

        if len(request.query_params) == 0 and user.is_authenticated:
            lon = user.coordinates.longitude
            lat = user.coordinates.latitude

            def distance_points(distance):
                if distance < 10:
                    return 20
                if distance < 20:
                    return 15
                if distance < 30:
                    return 10
                if distance < 40:
                    return 5
                if distance < 50:
                    return 3
                return 0

            def category_points(user, item):
                if item.category in user.userprofile.categories:
                    return 15
                else:
                    return 0

            # can be used either for last visited or for last liked
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

            def num_likes_points(item):
                return item.like_set.count()

            def note_mean_points(user):
                #mean = user.note_set.aggregate(Avg("note"))["note_avg"]
                mean_user_notes = User.objects.aggregate(Avg("userprofile__mean_note"))

                if user.mean_note > mean_user_notes:
                    return 5
                if user.mean_note == mean_user_notes:
                    return 3
                return 0

            def num_comments(item):
                n_comments = item.comment_set.count()
                mean = Comment.objects.aggregate(Avg("comment_set__mean_note"))
                return

            def num_offers(item):
                return item.offers_received.count()

            def compute_tot_points(distance_points, category_points, last_liked_points, last_visited_points,
                                   num_like_points, note_mean_points, num_comments_points, num_offers_points):
                return 20 * distance_points + \
                       15 * category_points + \
                       11 * last_liked_points + \
                       7 * last_visited_points + \
                       6 * last_liked_points + \
                       5 * note_mean_points + \
                       2 * num_comments_points + \
                       num_offers_points


            recent_consultations = user.consultation_set.order_by("date")[:10]

            """queryset = Item.objects.raw(
                "SELECT *, "
                "distance_points(compute_distance(%f, %f, users_coordinates.longitude, users_coordinates.latitude)) * 20 + "
                "categories_points() + "
                "AS points "
                "FROM items_item "
                "INNER JOIN auth_user ON owner_id = auth_user.id "
                "INNER JOIN users_coordinates ON auth_user.id = users_coordinates.user_id "
                "ORDER BY points DESC" % (lon, lat)
            )


            queryset = Item.objects.raw(
                "SELECT *, "
                "compute_distance(%f, %f, users_coordinates.longitude, users_coordinates.latitude) * 20 AS points "
                "FROM items_item "
                "INNER JOIN auth_user ON owner_id = auth_user.id "
                "INNER JOIN users_coordinates ON auth_user.id = users_coordinates.user_id "
                "ORDER BY points DESC" % (lon, lat)
            )"""

            queryset = Item.objects.annotate(
                distance_points=Func(
                    Func(lat, lon, F("owner__coordinates__latitude"), F("owner__coordinates__longitude"),
                              function="compute_distance", output_field=FloatField()),
                    function="distance_points", output_field=IntegerField()
                )
            ).order_by("-distance_points")

        else:
            queryset = filter_items(serializer.validated_data)

        return Response(AggregatedItemSerializer(queryset, many=True).data)

    def perform_create(self, serializer):
        price_min = serializer.validated_data.get("price_min", None)
        price_max = serializer.validated_data.get("price_max", None)

        check_prices(price_min, price_max)
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        price_min = serializer.validated_data.get("price_min", serializer.instance.price_min)
        price_max = serializer.validated_data.get("price_max", serializer.instance.price_max)

        check_prices(price_min, price_max)
        serializer.save()


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ImageViewSet(mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class LikeViewSet(mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
