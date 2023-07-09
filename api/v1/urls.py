from channels.routing import URLRouter
from django.urls import path, include

urlpatterns = [
    path("user_auth/", include("api.v1.user_auth.urls"))
]
