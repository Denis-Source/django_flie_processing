from channels.layers import get_channel_layer

from core.celery import app
from task.document.services import convert_file
from task.models import DocumentConversionTask
from task.on_demand import OnDemandTask


@app.task(bind=True, base=OnDemandTask)
def convert_document(self, task_id):
    task = DocumentConversionTask.objects.filter(id=task_id).first()
    converted_file = convert_file(task.input_file, task.output_format)
    task.set_output_file(converted_file)
