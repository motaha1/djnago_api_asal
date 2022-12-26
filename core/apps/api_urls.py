from django.urls import include, path

from core.apps.users import urls as user_urls

urlpatterns = [
    path(r'users/', include(user_urls.URLS)),
]