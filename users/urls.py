from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = "users"
urlpatterns = [
    url(r"^register/$", views.register_view, name="register"),
    url(r"^login/$", views.login_view, name="login"),
    url(r"^logout/$", views.logout_view, name="logout"),
    url(r"^account/$", views.account_view, name="account"),
    url(r"^api/login/$", views.api_login, name="api_login"),
    url(r"^api/logout/$", views.api_logout, name="api_logout"),
    url(r"^api/personal/$", views.get_personal_account_info, name="api_personal_info"),
    # For debug only csrf exempt
    url(r"^api/users/$", csrf_exempt(views.UsersAccounts.as_view()), name="users"),
    url(r"^api/users/(?P<pk>[0-9]+)/$", views.user_account, name="user"),
    url(r"^api/users/(?P<pk>[0-9]+)/username/$", views.UserNameUpdate, name="username"),
    url(r"^api/users/(?P<pk>[0-9]+)/firstname/$", views.UserFirstNameUpdate, name="firstname"),
    url(r"^api/users/(?P<pk>[0-9]+)/lastname/$", views.UserLastNameUpdate, name="lastname"),
    url(r"^api/users/(?P<pk>[0-9]+)/email/$", views.UserEMailUpdate, name="email"),
    url(r"^api/users/(?P<pk>[0-9]+)/password/$", views.UserPasswordUpdate, name="password"),
    url(r"^api/users/(?P<pk>[0-9]+)/accountactive/$", views.UserProfileAccountActiveUpdate, name="accountactive"),
]
