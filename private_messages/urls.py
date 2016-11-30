from django.conf.urls import url, include

from swapp.ShareAPIRootRouter import SharedAPIRootRouter
from . import views

router = SharedAPIRootRouter()
router.register(r'private_messages', views.MessageViewSet, base_name="private_messages")


app_name = "private_messages"
urlpatterns = [
    url(r'^', include(router.urls)),
]
