from django.db.models.signals import post_save
from django.dispatch import receiver
from django_eventstream import send_event

from api.v1.log_stream.serializers import LogStreamSerializer
from log_record.models import LogRecord


@receiver(post_save, sender=LogRecord)
def post_save_log_record(sender, instance, **kwargs):
    data = LogStreamSerializer(instance).data
    send_event("log_stream", "message", data)
