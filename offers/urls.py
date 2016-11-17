from django.conf.urls import url, include

from swapp.ShareAPIRootRouter import SharedAPIRootRouter
from . import views

router = SharedAPIRootRouter()
router.register(r'offers', views.OfferViewSet, base_name="offers")

app_name = "offers"
urlpatterns = [
    url(r'^', include(router.urls)),
]
