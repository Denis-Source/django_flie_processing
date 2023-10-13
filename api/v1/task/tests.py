from django.core.files.uploadedfile import SimpleUploadedFile

from api.tests import BaseAPITestCase
from task.models import Task, ConversionTask
from upload.models import Upload
from utils.generation import generate_document


class BaseListTaskTestCase(BaseAPITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.n = 100
        n_map = {
            0: Task.Statuses.CREATED,
            1: Task.Statuses.RUNNING,
            2: Task.Statuses.ERRORED,
            3: Task.Statuses.FINISHED,
            4: Task.Statuses.CREATED,
        }
        self.content, _ = generate_document()
        self.file = SimpleUploadedFile(
            "file.md",
            self.content
        )
        self.upload = Upload.objects.create(
            name="test.html",
            file=self.file,
            user=self.user
        )
        for i in range(self.n):
            task = ConversionTask(
                name="test",
                upload=self.upload,
                initiator=self.user
            )
            task.update_status(n_map[i % len(n_map)])
            task.save()
