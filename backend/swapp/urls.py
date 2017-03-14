"""
swapp URL Configuration
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"", include("pages.home.urls")),
    url(r"api/", include("users.urls")),
    url(r"api/", include("private_messages.urls")),
    url(r"api/", include("comments.urls")),
    url(r"api/", include("items.urls")),
    url(r"api/", include("offers.urls")),
    url(r"api/", include("notifications.urls"))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
