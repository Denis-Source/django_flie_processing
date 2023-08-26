from core.celery import app
from task.document.services import convert_file
from task.models import ConversionTask
from task.on_demand import OnDemandTask


@app.task(bind=True, base=OnDemandTask)
def convert_document(self, task_id):
    """Open a task that will convert input file into output"""
    task = ConversionTask.objects.filter(id=task_id).first()
    converted_file = convert_file(task.upload.file, task.output_format)
    task.set_output_file(converted_file)
