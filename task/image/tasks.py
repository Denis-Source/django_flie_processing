from core.celery import app
from task.image.serivces import convert_file
from task.models import ImageConversionTask
from task.on_demand import OnDemandTask


@app.task(bind=True, base=OnDemandTask)
def convert_image(self, task_id):
    """Open a task that will convert input file into output"""
    task = ImageConversionTask.objects.filter(id=task_id).first()
    converted_file = convert_file(
        task.input_file,
        task.output_format,
        quality=task.quality
    )
    task.set_output_file(converted_file)
