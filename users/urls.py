from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views

app_name = "users"

router = DefaultRouter()
router.register(r'notes', views.NoteViewSet)

urlpatterns = [
    #url(r"^register/$", views.register_view, name="register"),  # TODO delete when not used anymore
    #url(r"^login/$", views.login_view, name="login"),  # TODO delete when not used anymore
    #url(r"^logout/$", views.logout_view, name="logout"),  # TODO delete when not used anymore
    #url(r"^account/$", views.account_view, name="account"),  # TODO delete when not used anymore

    url(r"csrf/$", views.get_csrf_token, name="get_csrf"),
    url(r"login/$", views.Login.as_view(), name="login_user"),
    url(r"logout/$", views.logout_user, name="logout_user"),
    url(r"users/$", views.CreateUser.as_view(), name="create_user"),
    url(r"users/(?P<username>.+)/$", views.get_public_account_info, name="get_public_account_info"),
    url(r"account/$", views.UserAccount.as_view(), name="user_account"),
    url(r"account/password/", views.change_password, name="change_password"),
    url(r"account/location/", views.LocationView.as_view(), name="location"),
] + router.urls
