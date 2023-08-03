from logging import getLogger

from celery import Task as CeleryTask

from task.models import Task

logger = getLogger()


class OnDemandTask(CeleryTask):
    """Celery task that will sync with database one"""
    model_task_class = Task

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_task = None

    def before_start(self, _, args, kwargs):
        """Find database task and set its status to running"""
        self.db_task = self.model_task_class.objects.get(id=kwargs["task_id"])
        self.db_task.update_status(self.db_task.Statuses.RUNNING)

    def on_success(self, retval, task_id, args, kwargs):
        """Set database task status to finished"""
        self.db_task.update_status(Task.Statuses.FINISHED)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Set database task status to errored"""
        self.db_task.update_status(Task.Statuses.ERRORED)

    def on_timeout(self, soft_timeout, **kwargs):
        """Set database task status to canceled"""
        self.db_task.update_status(Task.Statuses.CANCELED)
