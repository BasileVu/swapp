from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"items", views.ItemViewSet, base_name="items")
router.register(r"categories", views.CategoryViewSet, base_name="categories")
router.register(r"likes", views.LikeViewSet, base_name="likes")
router.register(r"images", views.ImageViewSet, base_name="images")
router.register(r"deliverymethods", views.DeliveryMethodViewSet, base_name="delivery_methods")
urlpatterns = router.urls
