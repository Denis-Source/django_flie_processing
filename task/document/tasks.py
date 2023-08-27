from billiard.exceptions import SoftTimeLimitExceeded

from core.celery import app
from task.document.services import convert_file
from task.models import ConversionTask


@app.task(bind=True)
def convert_document(self, task_id):
    """Open a task that will convert input file into output"""
    task = ConversionTask.objects.filter(id=task_id).first()
    try:
        converted_file = convert_file(task.upload.file, task.output_format)
        task.set_output_file(converted_file)

    except SoftTimeLimitExceeded:
        task.update_status(ConversionTask.Statuses.CANCELED)

    except RuntimeError:
        task.update_status(ConversionTask.Statuses.ERRORED)