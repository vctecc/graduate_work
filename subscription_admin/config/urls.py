from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from config.settings import base


urlpatterns = [
    path('admin/', admin.site.urls),
] + static(base.STATIC_URL, document_root=base.STATIC_ROOT)
