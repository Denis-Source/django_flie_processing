from django.urls import path

from api.v1.log_stream.consumers import LogRecordStreamConsumer

event_urlpatterns = [
    path("", LogRecordStreamConsumer.as_asgi(), {"channels": ["log_stream"]})
]
