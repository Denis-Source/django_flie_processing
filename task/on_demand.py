from logging import getLogger

from celery import Task as CeleryTask

from task.models import Task

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
