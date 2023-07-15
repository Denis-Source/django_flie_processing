from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.v1.task.serializers import TaskSerializer
from task.models import Task


@receiver(post_save, sender=Task)
def task_post_save_receiver(sender, instance, created, **kwargs):
    data = TaskSerializer(instance).data
    channel_layer = get_channel_layer()
    if created:
        message_type = "opened_task"
    else:
        message_type = "updated_task"

    async_to_sync(channel_layer.group_send)(instance.initiator.username, {
        "type": message_type,
        "data": data
    })
