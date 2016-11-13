from django.conf.urls import url

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
    url(r"^api/users/$", views.create_account, name="users"),
    url(r"^api/users/(?P<pk>[0-9]+)/profile/$", views.UserProfileDetail.as_view(), name="user-profile-detail"),
]
