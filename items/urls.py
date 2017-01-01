from django.conf.urls import url

from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'items', views.ItemViewSet, base_name="items")
router.register(r'categories', views.CategoryViewSet, base_name="categories")
router.register(r'likes', views.LikeViewSet, base_name="likes")
router.register(r'images', views.ImageViewSet, base_name="images")
urlpatterns = router.urls
