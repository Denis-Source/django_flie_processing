from channels.routing import URLRouter
from django.urls import path

from api.event_urls import event_urlpatterns

event_urlpatterns = [
    path("api/", URLRouter(event_urlpatterns))
]
