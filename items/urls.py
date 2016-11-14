from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'api/items', views.ItemViewSet)
router.register(r'api/categories', views.CategoryViewSet)
router.register(r'api/likes', views.LikeViewSet)
router.register(r'api/images', views.ImageViewSet)

app_name = "items"
urlpatterns = [
    #url(r"^items/create/$", views.create_view, name="create_view"),
    #url(r"^items/(?P<item_id>\d+)/$", views.item_view, name="item_view"),
    #url(r"^api/items/$", views.create_item, name="create_item"),
    #url(r"^api/items/(?P<item_id>\d+)/$", views.get_item, name="get_item"),
    #url(r"^api/items/(?P<item_id>\d+)/archive$", views.archive_item, name="archive_item"),
    #url(r"^api/items/(?P<item_id>\d+)/unarchive$", views.unarchive_item, name="unarchive_item"),
    url(r'^', inclu de(router.urls)),
]
