import time
from logging import getLogger

from django.utils import timezone

from core.celery import app
from task.models import Task

logger = getLogger()

@app.task
def test_task(task_id):
    task = Task.objects.get(id=task_id)
    task.status = Task.Statuses.RUNNING
    task.save()
    time.sleep(10)
    task.status = task.Statuses.FINISHED
    task.closed_at = timezone.now()
    task.save()
