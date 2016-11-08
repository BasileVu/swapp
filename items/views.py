from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
import datetime

# Create your views here.
from django.urls import reverse
<<<<<<< HEAD
from django.views.decorators.http import require_http_methods, require_POST, require_GET
=======
from django.views.decorators.http import require_http_methods
>>>>>>> 27febc3... Add the REST API urls for archiving and unarchiving items

from items.models import Category, Item
from users.models import UserProfile


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


<<<<<<< HEAD
@require_POST
@login_required(login_url="users:login", redirect_field_name="")
def create_item(request):
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
        return JsonResponse({"error": "The minimum price is higher than the maximum price"}, status=400)

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


=======
>>>>>>> 27febc3... Add the REST API urls for archiving and unarchiving items
@require_http_methods(["PATCH"])
@login_required(login_url="users:login", redirect_field_name="")
def archive_item(request, item_id):
    try:
        Item.objects.filter(id=item_id, owner=UserProfile.objects.get(user=request.user).id).update(archived=1)
    except IntegrityError:
        return JsonResponse({"error": "User not logged in or item not found"}, status=409)

    response = HttpResponse()
<<<<<<< HEAD
    response["Location"] = "/api/items/%d/" % int(item_id)
    response.status_code = 200
=======
    response["Location"] = "/api/item/%d/" % int(item_id)
    response.status_code = 201
>>>>>>> 27febc3... Add the REST API urls for archiving and unarchiving items
    return response


@require_http_methods(["PATCH"])
@login_required(login_url="users:login", redirect_field_name="")
def unarchive_item(request, item_id):
    try:
        Item.objects.filter(id=item_id, owner=UserProfile.objects.get(user=request.user).id).update(archived=0)
    except IntegrityError:
        return JsonResponse({"error": "User not logged in or item not found"}, status=409)

    response = HttpResponse()
<<<<<<< HEAD
    response["Location"] = "/api/items/%d/" % int(item_id)
    response.status_code = 200
=======
    response["Location"] = "/api/item/%d/" % int(item_id)
    response.status_code = 201
>>>>>>> 27febc3... Add the REST API urls for archiving and unarchiving items
    return response
