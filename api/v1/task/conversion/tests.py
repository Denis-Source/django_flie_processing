import os

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

from api.tests import BaseAPITestCase
from api.v1.task.conversion import urls
from core.constants import IMAGE_INPUT_FORMATS, IMAGE_OUTPUT_FORMATS, DOCUMENT_INPUT_FORMATS, DOCUMENT_OUTPUT_FORMATS
from task.models import Task, ConversionTask
from upload.models import Upload
from utils.generation import generate_document, generate_noisy_image


class BaseConversionListTaskTestCase(BaseAPITestCase):
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


class ListConversionHistoryTestCase(BaseConversionListTaskTestCase):
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


class ListOpenedConversionTestCase(BaseConversionListTaskTestCase):
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


class RetrieveConversionFormatsViewTestCase(BaseAPITestCase):
    url_name = urls.FORMATS

    def setUp(self) -> None:
        super().setUp()
        self.expected = {
            Upload.MediaTypes.IMAGE: {
                "input_formats": IMAGE_INPUT_FORMATS,
                "output_formats": IMAGE_OUTPUT_FORMATS
            },
            Upload.MediaTypes.DOCUMENT: {
                "input_formats": DOCUMENT_INPUT_FORMATS,
                "output_formats": DOCUMENT_OUTPUT_FORMATS
            }
        }

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


class BaseDocumentConversionTaskTestCase(BaseAPITestCase):
    def setUp(self) -> None:
        super().setUp()

        self.input_format = ".html"
        self.output_format = "md"

        self.content, self.expected = generate_document()

        self.file = SimpleUploadedFile(
            "file.md",
            self.content
        )
        self.upload = Upload.objects.create(
            name="test.html",
            file=self.file,
            user=self.user
        )


class CreateDocumentConversionTaskTestCase(BaseDocumentConversionTaskTestCase):
    url_name = urls.CREATE

    def test_create_success(self):
        """Should create a task if data and credentials are correct"""
        response = self.client.post(
            self.get_url(),
            {
                "name": "test_task_1",
                "output_format": self.output_format,
                "upload": self.upload.id
            },
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["status"], Task.Statuses.CREATED)

    def test_create_unauthorized(self):
        """Should return unauthorized if credentials are not provided"""
        response = self.client.post(
            self.get_url(),
            {
                "name": "test_task_1",
                "output_format": self.output_format,
                "upload": self.upload.id
            },
        )
        self.assertEqual(response.status_code, 401)

    def test_missing_file(self):
        """Should return a bad request if file is not provided"""
        response = self.client.post(
            self.get_url(),
            {
                "name": "test_task_1",
                "output_format": self.output_format,
            },
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 400)

    def test_bad_data(self):
        """Should return a bad request if output format is wrong"""
        response = self.client.post(
            self.get_url(),
            {
                "name": "test_task_1",
                "output_format": "png",  # wrong format
                "upload": self.upload
            },
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 400)


class CreateImageConversionTaskTestCase(BaseAPITestCase):
    url_name = urls.CREATE

    def setUp(self) -> None:
        super().setUp()
        self.size = 100, 100
        self.image = Image.new("RGB", self.size, "white")
        self.image = generate_noisy_image(self.image)

        self.input_format = ".png"
        self.output_format = "jpeg"

        self.file = SimpleUploadedFile(
            "file.png",
            b""
        )

        self.image.save(self.file.name)

        self.upload = Upload.objects.create(
            name=self.file.name,
            user=self.user,
            file=self.file
        )

    def tearDown(self) -> None:
        super().tearDown()
        os.remove(self.file.name)

    def test_create_success(self):
        """Should create a task if data and credentials are correct"""
        response = self.client.post(
            self.get_url(),
            {
                "name": "test_task_1",
                "output_format": self.output_format,
                "upload": self.upload.id
            },
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["status"], Task.Statuses.CREATED)

    def test_create_unauthorized(self):
        """Should return unauthorized if credentials are not provided"""
        response = self.client.post(
            self.get_url(),
            {
                "name": "test_task_1",
                "output_format": self.output_format,
                "upload": self.upload.id
            },
        )
        self.assertEqual(response.status_code, 401)

    def test_missing_file(self):
        """Should return a bad request if file is not provided"""
        response = self.client.post(
            self.get_url(),
            {
                "name": "test_task_1",
                "output_format": self.output_format,
            },
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 400)

    def test_bad_data(self):
        """Should return a bad request if output format is wrong"""
        response = self.client.post(
            self.get_url(),
            {
                "name": "test_task_1",
                "output_format": "md",  # wrong format
                "upload": self.upload.id
            },
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 400)


class RetrieveConversionTaskTestCase(BaseDocumentConversionTaskTestCase):
    url_name = urls.RETRIEVE

    def setUp(self) -> None:
        super().setUp()

        self.data = {
            "name": "test_task",
            "output_format": "pdf",
            "upload": self.upload
        }

        self.user_task = ConversionTask.objects.create(
            initiator=self.user,
            **self.data
        )
        self.other_task = ConversionTask.objects.create(
            initiator=self.another_user,
            **self.data
        )

    def test_success(self):
        """Should return a task detail if credentials, task id and user initiator is correct"""
        response = self.client.get(
            self.get_url(id=self.user_task.id),
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user_task.id, response.json()["id"])

    def test_wrong_id(self):
        """Should return 404 if provided task does not exist"""
        non_existent_task_id = 200
        response = self.client.get(
            self.get_url(id=non_existent_task_id),
            headers=self.auth_headers
        )
        self.assertFalse(ConversionTask.objects.filter(id=non_existent_task_id).first())
        self.assertEqual(response.status_code, 404)

    def test_wrong_user(self):
        """Should return 404 if provided task exists, but it initiated by other user"""
        other_task_id = self.other_task.id
        response = self.client.get(
            self.get_url(id=other_task_id),
            headers=self.auth_headers
        )
        self.assertTrue(ConversionTask.objects.filter(id=other_task_id).exists())
        self.assertEqual(response.status_code, 404)

    def test_unauthorized(self):
        """Should return 401 if credentials are not provided"""
        response = self.client.get(
            self.get_url(id=self.user_task.id),
        )
        self.assertEqual(response.status_code, 401)
