import tempfile
from unittest import mock

from django.test import TestCase

from api.tests import BaseAPITestCase
from task.document.constants import INPUT_FORMATS, OUTPUT_FORMATS
from task.models import Task, DocumentConversionTask


class RetrieveDocumentFormatsViewTestCase(BaseAPITestCase):
    url_name = "v1-convert-document-formats"

    def setUp(self) -> None:
        super().setUp()
        self.expected = {
            "input_formats": INPUT_FORMATS,
            "output_formats": OUTPUT_FORMATS
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
            headers={"Authorization": f"Token {self.get_user_token_value()}"}
        )
        self.assertEqual(self.expected, response.json())

class CreateDocumentConversionTaskTestCase(BaseAPITestCase):
    url_name = "v1-convert-document-create"

    def setUp(self) -> None:
        super().setUp()
        self.content = b"<!DOCTYPE html>" \
                       b"<html>" \
                       b"<body>" \
                       b"<h1>First Heading</h1>" \
                       b"<p>First paragraph.</p>" \
                       b"</body>" \
                       b"</html>"
        self.expected = "# First Heading\n\n" \
                        "First paragraph.\n"

        self.input_format = ".html"
        self.output_format = "md"

        self.temp_input = tempfile.NamedTemporaryFile(delete=False, suffix=self.input_format)
        self.temp_input.write(self.content)
        self.temp_input.close()

    def test_create_success(self):
        with open(self.temp_input.name) as f:
            response = self.client.post(
                self.get_url(),
                {
                    "name": "test_task_1",
                    "output_format": self.output_format,
                    "input_file": f
                },
                headers={"Authorization": f"Token {self.get_user_token_value()}"}
            )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["status"], Task.Statuses.CREATED)

    def test_create_unauthorized(self):
        with open(self.temp_input.name) as f:
            response = self.client.post(
                self.get_url(),
                {
                    "name": "test_task_1",
                    "output_format": self.output_format,
                    "input_file": f
                },
            )
        self.assertEqual(response.status_code, 401)

    def test_missing_file(self):
        with open(self.temp_input.name) as f:
            response = self.client.post(
                self.get_url(),
                {
                    "name": "test_task_1",
                    "output_format": self.output_format,
                },
                headers={"Authorization": f"Token {self.get_user_token_value()}"}
            )
        self.assertEqual(response.status_code, 400)


    def test_bad_data(self):
        with open(self.temp_input.name) as f:
            response = self.client.post(
                self.get_url(),
                {
                    "name": "test_task_1",
                    "output_format": "png", # wrong format
                    "input_file": f
                },
                headers={"Authorization": f"Token {self.get_user_token_value()}"}
            )
        self.assertEqual(response.status_code, 400)
