from channels.routing import URLRouter
from django.urls import path

from api.v1.event_urls import event_urlpatterns

event_urlpatterns = [
    path("v1/", URLRouter(event_urlpatterns))
]
