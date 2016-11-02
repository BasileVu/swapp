from django.conf.urls import url

from . import views

app_name = "items"
urlpatterns = [
    url(r"^item/create/$", views.create_view, name="create"),
    url(r"^item/$", views.item_view, name="item"),
]
