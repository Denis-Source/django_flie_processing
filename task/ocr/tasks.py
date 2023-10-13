from core.celery import app
from task.models import ConversionTask, OCRTask
from task.ocr.services import get_text_from_file


@app.task(bind=True)
def get_text(self, task_id):
    """Open a task that will convert input file into output"""
    task = OCRTask.objects.filter(id=task_id).first()
    # try:
    converted_file = get_text_from_file(
        input_file=task.upload.file,
        languages=[task.language]
    )
    task.set_output(converted_file)
    # except Exception as e:
        # task.update_status(ConversionTask.Statuses.ERRORED)
