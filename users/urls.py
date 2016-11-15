from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = "users"
urlpatterns = [
    url(r"^register/$", views.register_view, name="register"),  # TODO delete when not used anymore
    url(r"^login/$", views.login_view, name="login"),  # TODO delete when not used anymore
    url(r"^logout/$", views.logout_view, name="logout"),  # TODO delete when not used anymore
    url(r"^account/$", views.account_view, name="account"),  # TODO delete when not used anymore
    url(r"^api/login/$", views.login_user, name="login_user"),
    url(r"^api/logout/$", views.logout_user, name="logout_user"),
    url(r"^api/users/$", csrf_exempt(views.create_user), name="create_user"),  # FIXME csrf_exempt debug
    url(r"^api/account/$", views.UserAccount.as_view(), name="user_account"),
    url(r"^api/account/password", views.change_password, name="change_password"),
]
