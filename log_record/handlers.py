from asyncio import get_event_loop
from logging import Handler

from asgiref.sync import sync_to_async
from django.core.exceptions import SynchronousOnlyOperation


class LogRecordHandler(Handler):
    def emit(self, record) -> None:
        # from log_record.models import LogRecord
        #
        # log_record = LogRecord(
        #     name=record.name,
        #     level=record.levelno,
        #     message=record.message
        # )
        #
        # try:
        #     log_record.save()
        # except SynchronousOnlyOperation:
        #     loop = get_event_loop()
        #     loop.create_task(sync_to_async(log_record.save)())
        pass
