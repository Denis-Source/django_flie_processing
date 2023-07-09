import logging

from django_eventstream.consumers import EventsConsumer


class LogRecordStreamConsumer(EventsConsumer):
    async def handle(self, body, **kwargs):
        return await super().handle(body, **kwargs)
