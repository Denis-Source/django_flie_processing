from channels.routing import URLRouter
from django.urls import path

from api.v1.ws_urls import urlpatterns

urlpatterns = [
    path("v1/", URLRouter(urlpatterns))
]
