import math

from django.db.models import Q
from django.db import connection, transaction
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from items.models import Like
from items.serializers import *
from swapp import settings


# TODO : Validators for example price_min < price_max : http://www.django-rest-framework.org/api-guide/validators/
from swapp.gmaps_api_utils import compute_distance


def get_item_ids_near(latitude, longitude, radius):
    connection.connection.create_function('compute_distance', 4, compute_distance)

    query = """
        SELECT items_item.id,
          compute_distance(%f, %f, users_coordinates.latitude, users_coordinates.longitude) AS distance
        FROM items_item
          INNER JOIN auth_user ON items_item.owner_id = auth_user.id
          INNER JOIN users_coordinates ON auth_user.id = users_coordinates.user_id
        WHERE distance < %d;""" % (latitude, longitude, radius)

    return [i.id for i in Item.objects.raw(query)]


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return AggregatedItemSerializer
        return ItemSerializer

    def list(self, request, *args, **kwargs):
        serializer = SearchItemsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        q = serializer.validated_data["q"]
        price_min = serializer.validated_data["price_min"]
        price_max = serializer.validated_data["price_max"]
        category = serializer.validated_data["category"]
        lat = serializer.validated_data["lat"]
        lon = serializer.validated_data["lon"]
        radius = serializer.validated_data["radius"]

        queryset = Item.objects.filter(
            Q(name__icontains=q) | Q(description__icontains=q),
            price_min__gte=price_min
        )

        if category is not None:
            category_list = Category.objects.filter(name=category)
            queryset = queryset.filter(category__in=category_list)

        if price_max is not None:
            queryset = queryset.filter(price_max__lte=int(price_max))

        if lat is not None and lon is not None:
            if radius is None:
                radius = 100000  # FIXME earth perimeter/2
            queryset = queryset.filter(id__in=get_item_ids_near(float(lat), float(lon), float(radius)))

        return Response(AggregatedItemSerializer(queryset, many=True).data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


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
