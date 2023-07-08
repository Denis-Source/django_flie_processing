from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg.openapi import Info
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

from core import settings

schema_view = get_schema_view(
    Info(
        title="Snippets API",
        default_version='v1',
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls"))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
