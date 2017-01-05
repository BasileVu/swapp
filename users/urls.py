from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views

app_name = "users"

router = DefaultRouter()
router.register(r"notes", views.NoteViewSet)
router.register(r"account/categories", views.CategoryViewSet, base_name="interested_by_categories")

urlpatterns = [
    url(r"csrf/$", views.get_csrf_token, name="get_csrf"),
    url(r"login/$", views.login_user, name="login_user"),
    url(r"logout/$", views.logout_user, name="logout_user"),
    url(r"users/$", views.create_user, name="create_user"),
    url(r"users/(?P<username>.+)/$", views.get_public_account_info, name="get_public_account_info"),
    url(r"account/$", views.UserAccount.as_view(), name="user_account"),
    url(r"account/password/", views.change_password, name="change_password"),
    url(r"account/location/", views.LocationView.as_view(), name="location"),
] + router.urls
