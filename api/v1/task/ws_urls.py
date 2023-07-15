from channels.routing import URLRouter
from django.urls import path

from api.v1.task.consumers import TaskConsumer
from websocket.middlewares import TokenAuthMiddleware

urlpatterns = URLRouter([
    path("", TokenAuthMiddleware(TaskConsumer.as_asgi()))
])
