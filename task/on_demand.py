from logging import getLogger

from asgiref.sync import async_to_sync
from celery import Task as CeleryTask
from channels.layers import get_channel_layer

from api.v1.task.consumers import TaskMessageTypes
from core.celery import app
from task.maze.utils import base64_file
from task.models import MazeGenerationTask, Task
from task.services import generate_image_stream, prepare_data
from websocket.general import construct

logger = getLogger()


class OnDemandTask(CeleryTask):
    model_task_class = Task

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_task = None

    def before_start(self, _, args, kwargs):
        self.db_task = self.model_task_class.objects.get(id=kwargs["task_id"])
        self.db_task.update_status(self.db_task.Statuses.RUNNING)

    def on_success(self, retval, task_id, args, kwargs):
        self.db_task.update_status(Task.Statuses.FINISHED)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        self.db_task.update_status(Task.Statuses.ERRORED)

    def on_timeout(self, soft_timeout, **kwargs):
        self.db_task.update_status(Task.Statuses.CANCELED)


class OnDemandGenerateMazeTask(OnDemandTask):
    model_task_class = MazeGenerationTask


@app.task(bind=True, base=OnDemandGenerateMazeTask)
def generate_maze(self, task_id):
    channel_layer = get_channel_layer()
    for image64 in generate_image_stream(
        self.db_task.columns,
        self.db_task.rows,
        self.db_task.scale,
        self.db_task.algorithm,
    ):
        async_to_sync(channel_layer.group_send)(
            self.db_task.initiator.username,
            construct(
                TaskMessageTypes.UPDATED,
                prepare_data(self.db_task, extra={"image": image64})
            ))
    else:
        self.db_task.set_result(base64_file(image64))
