from django.conf.urls import url

from . import views

app_name = "items"
urlpatterns = [
    url(r"^create/$", views.create_view, name="create"),
    url(r"^(?P<item_id>\d+)/$", views.item_view, name="item"),
    url(r"^(?P<item_id>\d+)/archive$", views.archive_item, name="archive"),
    url(r"^(?P<item_id>\d+)/unarchive$", views.unarchive_item, name="unarchive"),
]
