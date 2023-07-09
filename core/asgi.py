"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

import django_eventstream
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path, re_path

os.environ.setdefault("BASE_PATH", os.path.dirname(os.path.dirname(__file__)))


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": URLRouter([
        path("logs/", AuthMiddlewareStack(
            URLRouter(django_eventstream.routing.urlpatterns)
        ), { "channels": ["log_stream"] }),
        re_path(r"", get_asgi_application()),
    ]),
})
