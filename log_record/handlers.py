from logging import Handler


class LogRecordHandler(Handler):
    def emit(self, record) -> None:
        from log_record.models import LogRecord

        log_record = LogRecord(
            name=record.name,
            level=record.levelno,
            message=record.message
        )

        log_record.save()