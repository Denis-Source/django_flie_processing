from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

from api.tests import BaseAPITestCase
from api.v1.task.ocr import urls
from core import settings
from task.models import Task, OCRTask
from task.ocr.data.samples import ENG_TEST_IMAGE
from upload.models import Upload


class BaseListOCRTasksTestCase(BaseAPITestCase):
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
        self.file = open(settings.BASE_DIR.joinpath(ENG_TEST_IMAGE), "rb")
        self.file_name = "sample.png"

        self.upload = Upload.objects.create(
            name=self.file_name,
            file=File(self.file, self.file_name),
            user=self.user
        )
        for i in range(self.n):
            task = OCRTask(
                name="test",
                upload=self.upload,
                initiator=self.user,
                language=OCRTask.Languages.ENGLISH
            )
            task.update_status(n_map[i % len(n_map)])
            task.save()

    def tearDown(self) -> None:
        super().tearDown()
        self.file.close()


class OCRListTaskTestCase(BaseListOCRTasksTestCase):
    url_name = urls.HISTORY

    def test_history_success(self):
        """Should retrieve a list of task history"""
        response = self.client.get(
            self.get_url(),
            {
                "page_size": self.n
            },
            headers=self.auth_headers
        )
        self.assertTrue(len(Task.get_closed_tasks().filter(initiator=self.user)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], Task.get_closed_tasks().filter(initiator=self.user).count())

    def test_history_unauthorized(self):
        """Should return unauthorized if token is not provided"""
        response = self.client.get(
            self.get_url()
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ListOpenedOCRTasks(BaseListOCRTasksTestCase):
    url_name = urls.OPENED

    def test_opened_success(self):
        """Should retrieve a list of opened tasks"""
        response = self.client.get(
            self.get_url(),
            headers=self.auth_headers
        )
        self.assertTrue(len(Task.get_closed_tasks().filter(initiator=self.user)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Task.get_opened_tasks().filter(initiator=self.user).count())

    def test_opened_unauthorized(self):
        """Should return unauthorized if token is not provided"""
        response = self.client.get(
            self.get_url(),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RetrieveLanguagesViewTestCase(BaseAPITestCase):
    url_name = urls.LANGUAGES

    def setUp(self) -> None:
        super().setUp()
        self.expected = {value: label for value, label in OCRTask.Languages.choices}

    def test_unauthorized_success(self):
        """Should return a list of available format if user is not authorized"""

        response = self.client.get(
            self.get_url(),
        )
        self.assertEqual(self.expected, response.json())

    def test_authorized_success(self):
        """Should return a list of available formant if user is authorized"""
        response = self.client.get(
            self.get_url(),
            headers=self.auth_headers
        )
        self.assertEqual(self.expected, response.json())


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
