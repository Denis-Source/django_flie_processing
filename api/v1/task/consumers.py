from enum import Enum

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from websocket.general import construct


class TaskMessageTypes(str, Enum):
    OPENED = "opened_task"
    UPDATED = "updated_task"


class TaskConsumer(AsyncJsonWebsocketConsumer):
    """
    Websocket consumer that will send updates regarding task creation or updates
    """

    async def connect(self):
        """Add connected user to a consumer group, list current (unfinished) tasks"""
        from rest_framework.authtoken.admin import User
        user = self.scope.get("user")
        if type(user) == User:
            await self.channel_layer.group_add(user.username, self.channel_name)
            await self.accept()
        else:
            await self.close(4000)
            return

        tasks = await database_sync_to_async(self.get_unfinished_tasks)()
        for task_data in tasks:
            await self.send_json(
                construct(TaskMessageTypes.OPENED, task_data))

    async def opened_task(self, data):
        """Notify user that task was created"""
        await self.send_json(data)

    async def updated_task(self, data):
        """Notify user that task was updated"""
        await self.send_json(data)

    def get_unfinished_tasks(self):
        """List tasks that are opened"""
        from task.models import Task
        from api.v1.task.serializers import TaskSerializer

        tasks = Task.get_opened_tasks()
        return [TaskSerializer(task).data for task in tasks]
