"""
swapp URL Configuration
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from swapp.ShareAPIRootRouter import SharedAPIRootRouter


def api_urls():
    return SharedAPIRootRouter.shared_router.urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('pages.home.urls')),
    url(r'', include('users.urls')),
    url(r'api/', include(api_urls())),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
