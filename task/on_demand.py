import base64
from logging import getLogger

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.files.base import ContentFile

from api.v1.task.consumers import TaskMessageTypes
from api.v1.task.serializers import TaskSerializer
from core.celery import app
from task.maze.maze import Maze
from task.maze.utils import convert_to_64
from task.models import MazeGenerationTask
from websocket.general import construct

logger = getLogger()


@app.task
def generate_maze_task(task_id):
    channel_layer = get_channel_layer()

    task = MazeGenerationTask.objects.get(id=task_id)
    task.update_status(MazeGenerationTask.Statuses.RUNNING)
    maze = Maze(task.width, task.height, task.width * 12, task.height * 12, line_width=5)

    image = None

    data = TaskSerializer(task).data
    for image in maze.produce_maze_visualization(task.algorithm, 20):
        data["extra"] = {
            "image": (convert_to_64(image))
        }
        async_to_sync(channel_layer.group_send)(
            task.initiator.username,
            construct(TaskMessageTypes.UPDATED, data))

    task.update_status(MazeGenerationTask.Statuses.FINISHED)
    if image:
        task.set_result(image)
