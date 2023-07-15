from core.celery import app
from task.models import Task


@app.task
def cancel_stale_tasks():
    tasks = Task.get_stale_tasks()
    for task in tasks:
        task.update_status(Task.Statuses.CANCELED)
