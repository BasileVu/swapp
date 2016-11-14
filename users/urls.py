from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = "users"
urlpatterns = [
<<<<<<< HEAD
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
    url(r"^api/users/(?P<pk>[0-9]+)/username/$", views.UserName.as_view(), name="username"),
    url(r"^api/users/(?P<pk>[0-9]+)/firstname/$", views.UserFirstName.as_view(), name="firstname"),
    url(r"^api/users/(?P<pk>[0-9]+)/lastname/$", views.UserLastName.as_view(), name="lastname"),
    url(r"^api/users/(?P<pk>[0-9]+)/email/$", views.UserEmail.as_view(), name="email"),
    url(r"^api/users/(?P<pk>[0-9]+)/password/$", views.UserPassword.as_view(), name="password"),
    url(r"^api/users/(?P<pk>[0-9]+)/accountactive/$", views.UserProfileAccountActive.as_view(), name="accountactive"),
    url(r"^api/users/(?P<pk>[0-9]+)/location/$", views.UserProfileLocation.as_view(), name="location"),
=======
    url(r"^register/$", views.register_view, name="register"),  # TODO delete when not used anymore
    url(r"^login/$", views.login_view, name="login"),  # TODO delete when not used anymore
    url(r"^logout/$", views.logout_view, name="logout"),  # TODO delete when not used anymore
    url(r"^account/$", views.account_view, name="account"),  # TODO delete when not used anymore
    url(r"^api/login/$", views.login_user, name="login_user"),
    url(r"^api/logout/$", views.logout_user, name="logout_user"),
    url(r"^api/users/$", csrf_exempt(views.create_user), name="create_user"),  # FIXME csrf_exempt debug
    url(r"^api/account/$", views.UserAccount.as_view(), name="user_account"),
    url(r"^api/account/password", views.change_password, name="change_password"),
>>>>>>> 00c6a9d... user-rest improvement
]

# TODO delete
"""
    url(r"^api/account/username/$", views.UserName.as_view(), name="username"),
    url(r"^api/account/first_name/$", views.UserFirstName.as_view(), name="first_name"),
    url(r"^api/account/last_name/$", views.UserLastName.as_view(), name="last_name"),
    url(r"^api/account/email/$", views.UserEmail.as_view(), name="email"),
    url(r"^api/account/password/$", views.UserPassword.as_view(), name="password"),
    url(r"^api/account/account_active/$", views.UserProfileAccountActive.as_view(), name="account_active"),
"""
