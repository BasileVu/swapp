from django.db.models import F, FloatField
from django.db.models import Func
from django.db.models import Q
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from items.serializers import *
from users.models import Consultation


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def check_prices(self, price_min, price_max):
        if price_min is not None and price_min < 0:
            raise ValidationError("Price min is negative")

        if price_max is not None and price_max < 0:
            raise ValidationError("Price max is negative")

        if price_min is not None and price_max is not None and price_min > price_max:
            raise ValidationError("Price min is higher than price max")

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

        q = serializer.validated_data["q"]
        category = serializer.validated_data["category"]
        price_min = serializer.validated_data["price_min"]
        price_max = serializer.validated_data["price_max"]
        lat = serializer.validated_data["lat"]
        lon = serializer.validated_data["lon"]
        radius = serializer.validated_data["radius"]
        order_by = serializer.validated_data["order_by"]

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

        return Response(AggregatedItemSerializer(queryset, many=True).data)

    def perform_create(self, serializer):
        price_min = serializer.validated_data.get("price_min", None)
        price_max = serializer.validated_data.get("price_max", None)

        self.check_prices(price_min, price_max)
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        price_min = serializer.validated_data.get("price_min", serializer.instance.price_min)
        price_max = serializer.validated_data.get("price_max", serializer.instance.price_max)

        self.check_prices(price_min, price_max)
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

'''
@login_required(login_url="users:login", redirect_field_name="")
def create_view(request):
    try:
        name = request.POST["name"]
        description = request.POST["description"]
        price_min = int(request.POST["price_min"])
        price_max = int(request.POST["price_max"])
        archived = 0
        category = request.POST["category"]
    except KeyError:
        return render(request, "items/create.html", {'categories': Category.objects.all()})
    if price_min > price_max:
        return render(request, "users/create.html", {
            'categories': Category.objects.all(),
            "error_message": "Price min is higher than price max."
        })
    try:
        item = Item(name=name, description=description, price_min=price_min, price_max=price_max,
                    archived=archived,
                    category=Category.objects.get(id=category),
                    owner=UserProfile.objects.get(user=request.user))
        item.save()
    except IntegrityError:
        return render(request, "items/create.html", {
            'categories': Category.objects.all(),
            "error_message": "Item already exists."
        })
    return HttpResponseRedirect('/items/%s/' % item.id)


def item_view(request, item_id):
    return render(request, "items/item.html", {"item": Item.objects.get(id=item_id)})


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def create_item(request):
    try:
        received_json_data = json.loads(request.body.decode("utf-8"))
        name = received_json_data["name"]
        description = received_json_data["description"]
        price_min = int(received_json_data["price_min"])
        price_max = int(received_json_data["price_max"])
        archived = 0
        category = int(received_json_data["category"])
    except KeyError:
        return JsonResponse({"error": "Error in the JSON data"}, status=400)
    if price_min > price_max:
        return JsonResponse({"error": "The minimum price is higher than the maximum price"}, status=400)

    if request.user.userprofile.location == "":
        return JsonResponse({"error": "Your location is not specified"}, status=400)

    try:
        item = Item(name=name, description=description, price_min=price_min, price_max=price_max,
                    archived=archived,
                    category=Category.objects.get(id=category),
                    owner=UserProfile.objects.get(user=request.user))
        item.save()
    except IntegrityError:
        return JsonResponse({"error": "Error creating the item"}, status=400)

    response = HttpResponse()
    response["Location"] = "/api/items/%d/" % item.id
    response.status_code = 201
    return response


@api_view(["GET"])
def get_item(request, item_id):
    return JsonResponse(Item.objects.get(id=item_id), status=200)


@api_view(["PATCH"])
@login_required(login_url="users:login", redirect_field_name="")
def archive_item(request, item_id):
    try:
        Item.objects.filter(id=item_id, owner=UserProfile.objects.get(user=request.user).id).update(archived=1)
    except IntegrityError:
        return JsonResponse({"error": "User not logged in or item not found"}, status=409)

    response = HttpResponse()
    response["Location"] = "/api/items/%d/" % int(item_id)
    response.status_code = 200
    return response


@api_view(["PATCH"])
@login_required(login_url="users:login", redirect_field_name="")
def unarchive_item(request, item_id):
    try:
        Item.objects.filter(id=item_id, owner=UserProfile.objects.get(user=request.user).id).update(archived=0)
    except IntegrityError:
        return JsonResponse({"error": "User not logged in or item not found"}, status=409)

    response = HttpResponse()
    response["Location"] = "/api/items/%d/" % int(item_id)
    response.status_code = 200

    return response
'''
