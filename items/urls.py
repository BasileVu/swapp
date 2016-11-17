from django.conf.urls import url, include

from swapp.ShareAPIRootRouter import SharedAPIRootRouter
from . import views

router = SharedAPIRootRouter()
router.register(r'items', views.ItemViewSet, base_name="items")
router.register(r'categories', views.CategoryViewSet, base_name="categories")
router.register(r'likes', views.LikeViewSet, base_name="likes")
router.register(r'images', views.ImageViewSet, base_name="images")


app_name = "items"
urlpatterns = [
    #url(r"^items/create/$", views.create_view, name="create_view"),
    #url(r"^items/(?P<item_id>\d+)/$", views.item_view, name="item_view"),
    #url(r"^api/items/$", views.create_item, name="create_item"),
    #url(r"^api/items/(?P<item_id>\d+)/$", views.get_item, name="get_item"),
    #url(r"^api/items/(?P<item_id>\d+)/archive$", views.archive_item, name="archive_item"),
    #url(r"^api/items/(?P<item_id>\d+)/unarchive$", views.unarchive_item, name="unarchive_item"),
    url(r'^', include(router.urls)),
]
