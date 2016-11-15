from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'api/offers', views.OfferViewSet)

app_name = "offers"
urlpatterns = [
    url(r'^', include(router.urls)),
]
