import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.conf import settings
from django.core.asgi import get_asgi_application
from django.urls import path, re_path
from core.event_urls import event_urlpatterns

os.environ.setdefault("BASE_PATH", os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter({
    "http": URLRouter([
        path("", URLRouter(event_urlpatterns)),
        re_path("", get_asgi_application()),
    ]),
})

