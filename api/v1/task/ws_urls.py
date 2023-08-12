from django.urls import path

from api.v1.task.consumers import TaskConsumer
from websocket.middlewares import JWTAuthMiddleware

urlpatterns = [
    path("", JWTAuthMiddleware(TaskConsumer.as_asgi()))
]
