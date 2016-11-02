from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
import datetime

# Create your views here.
from django.urls import reverse

from items.models import Category, Item


@login_required(login_url="users:login", redirect_field_name="")
def create_view(request):
    try:
        name = request.POST["name"]
        description = request.POST["description"]
        price_min = request.POST["price_min"]
        price_max = request.POST["price_max"]
        creation_date = datetime.datetime.now().time()
        archived = 0
        category = request.POST["category"]
    except KeyError:
        return render(request, "items/create.html", {'categories': Category.objects.all()})
    if price_min > price_max:
        return render(request, "users/register.html", {
            "error_message": "Price min is higher than price max."
        })

    try:
        item = User.objects.create_user(name, description, price_min, price_max, creation_date, archived, category, request.user.id)
    except IntegrityError:
        return render(request, "items/create.html", {
            'categories': Category.objects.all(),
            "error_message": "Item already exists."
        })

    item(request, item)
    return HttpResponseRedirect(reverse("items:item"))


def item_view(request):
    return render(request, "item/item.html", {"item": ""})

