from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

from api.tests import BaseAPITestCase
from api.v1.task.ocr import urls
from core import settings
from task.models import Task
from task.ocr.data.samples import ENG_TEST_IMAGE
from upload.models import Upload


class CreateOCRTaskTestCase(BaseAPITestCase):
    url_name = urls.CREATE

    def setUp(self) -> None:
        super().setUp()
        self.file = open(settings.BASE_DIR.joinpath(ENG_TEST_IMAGE), "rb")
        self.upload = Upload.objects.create(
            name=self.file.name,
            user=self.user,
            file=File(self.file, "image.png")
        )

    def tearDown(self) -> None:
        super().tearDown()
        self.file.close()

    def test_create_success(self):
        response = self.client.post(
            self.get_url(),
            {
                "name": "test_task_1",
                "upload": self.upload.id,
                "language": "eng"
            },
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["status"], Task.Statuses.CREATED)

    def test_create_wrong_upload_type(self):
        document_upload = Upload.objects.create(
            name="file.md",
            file=SimpleUploadedFile(
                "file.md",
                b"#hello\nworld\n"
            ),
            user=self.user
        )
        response = self.client.post(
            self.get_url(),
            {
                "name": "test_task_1",
                "upload": document_upload.id,
                "language": "eng"
            },
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 400)
