from channels.routing import URLRouter
from django.urls import path

from api.v1.task.ws_urls import urlpatterns

urlpatterns = [
    path("task/", URLRouter(urlpatterns))
]
