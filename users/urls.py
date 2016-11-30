from django.conf.urls import url

from swapp.ShareAPIRootRouter import SharedAPIRootRouter
from . import views

def api_urls():
    return SharedAPIRootRouter.shared_router.urls

app_name = "users"
urlpatterns = [
    url(r"^register/$", views.register_view, name="register"),  # TODO delete when not used anymore
    url(r"^login/$", views.login_view, name="login"),  # TODO delete when not used anymore
    url(r"^logout/$", views.logout_view, name="logout"),  # TODO delete when not used anymore
    url(r"^account/$", views.account_view, name="account"),  # TODO delete when not used anymore

    url(r"^api/csrf/$", views.get_csrf_token, name="get_csrf"),
    url(r"^api/login/$", views.login_user, name="login_user"),
    url(r"^api/logout/$", views.logout_user, name="logout_user"),
    url(r"^api/users/$", views.create_user, name="create_user"),
    url(r"^api/account/$", views.UserAccount.as_view(), name="user_account"),
    url(r"^api/account/password", views.change_password, name="change_password"),
    url(r"^api/account/location", views.LocationView.as_view(), name="location"),
]
