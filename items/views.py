import json

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from rest_framework import generics

from items.models import Category, Item
from items.serializers import ItemSerializer
from users.models import UserProfile


class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


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


@require_POST
@login_required(login_url="users:login", redirect_field_name="")
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
        return JsonResponse({"error": "Error, the minimum price is higher than the maximum price"}, status=400)

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


@require_GET
def get_item(request, item_id):
    return JsonResponse(Item.objects.get(id=item_id), status=200)


@require_http_methods(["PATCH"])
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


@require_http_methods(["PATCH"])
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
