from core.celery import app
from task.image.serivces import convert_file
from task.models import ConversionTask


@app.task(bind=True)
def convert_image(self, task_id):
    """Open a task that will convert input file into output"""
    task = ConversionTask.objects.filter(id=task_id).first()
    try:
        converted_file = convert_file(
            input_file=task.upload.file,
            frmt=task.output_format,
            quality=task.quality
        )
        task.set_output_file(converted_file)
    except Exception as e:
        task.update_status(ConversionTask.Statuses.ERRORED)