from channels.routing import URLRouter
from django.urls import path

from .log_stream.event_urls import event_urlpatterns

event_urlpatterns = [
    path("log_stream/", URLRouter(event_urlpatterns))
]
