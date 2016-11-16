from django.db.models import Q
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response

from items.models import Like
from items.serializers import *


# TODO : Validators for example price_min < price_max : http://www.django-rest-framework.org/api-guide/validators/


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def list(self, request, *args, **kwargs):
        q = self.request.query_params.get("q", "")
        category_name = self.request.query_params.get("category", None)
        latitude = self.request.query_params.get("lat", 0)  # TODO
        longitude = self.request.query_params.get("lon", 0)  # TODO
        price_min = self.request.query_params.get("price_min", 0)
        price_max = self.request.query_params.get("price_max", None)
        order_by = self.request.query_params.get("order_by", None)  # TODO
        limit = self.request.query_params.get("limit", None)  # TODO
        page = self.request.query_params.get("page", None)  # TODO

        queryset = Item.objects.filter(
            Q(name__icontains=q) | Q(description__icontains=q),
            price_min__gte=int(price_min)
        )

        if category_name is not None:
            category_list = Category.objects.filter(name=category_name)
            queryset = queryset.filter(category__in=category_list)

        if price_max is not None:
            queryset = queryset.filter(price_max__lte=int(price_max))

        return Response(ItemSerializer(queryset, many=True).data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.userprofile)

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method == 'PUT' or request.method == "PATCH" or request.method == "DELETE":
            return view.owner == request.user
        if request.method == 'POST':
            return request.user.is_authenticated()


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
