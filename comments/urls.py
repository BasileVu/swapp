from django.conf.urls import url, include

from swapp.ShareAPIRootRouter import SharedAPIRootRouter
from . import views

router = SharedAPIRootRouter()
router.register(r'comments', views.CommentViewSet, base_name="comments")


app_name = "comments"
urlpatterns = [
    url(r'^', include(router.urls)),
]
