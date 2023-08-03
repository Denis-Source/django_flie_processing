from core.celery import app
from task.models import Task


@app.task
def cancel_stale_tasks():
    """Periodically searches stale tasks and deletes them"""
    tasks = Task.get_stale_tasks()
    for task in tasks:
        task.update_status(Task.Statuses.CANCELED)
