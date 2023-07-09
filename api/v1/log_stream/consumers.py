from django_eventstream import EventPermissionError, EventRequest
from django_eventstream.consumers import EventsConsumer, Listener
from rest_framework import status
from rest_framework.response import Response


class LogRecordStreamConsumer(EventsConsumer):
    def __init__(self):
        self.listener = Listener()

    async def parse_request(self, request):
        self.user = request.user
        if request.user.is_staff:
            return await super().parse_request(request)
        else:
            raise EventRequest.Error
