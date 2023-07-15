from channels.routing import URLRouter
from django.urls import path

from api.ws_urls import urlpatterns

urlpatterns = [
    path("api/", URLRouter(urlpatterns))
]
