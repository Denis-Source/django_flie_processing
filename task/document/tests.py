import os
import tempfile

from django.test import TestCase

from core import settings
from task.document.services import convert_path, convert_file


class DocumentTestCase(TestCase):
    def setUp(self) -> None:
        self.content = b"<!DOCTYPE html>" \
                       b"<html>" \
                       b"<body>" \
                       b"<h1>First Heading</h1>" \
                       b"<p>First paragraph.</p>" \
                       b"</body>" \
                       b"</html>"
        self.expected = "# First Heading\n\n" \
                        "First paragraph.\n"

        self.input_suffix = ".html"
        self.output_suffix = ".md"

        self.temp_input = tempfile.NamedTemporaryFile(delete=False, suffix=self.input_suffix)
        self.temp_input.write(self.content)
        self.temp_input.close()
        self.temp_output = tempfile.NamedTemporaryFile(delete=False, suffix=self.output_suffix)
        self.temp_output.close()

    def tearDown(self):
        super().tearDown()
        os.remove(self.temp_input.name)
        os.remove(self.temp_output.name)

    def test_convert_paths(self):
        """Should convert document into a specified format using paths"""
        convert_path(self.temp_input.name, "markdown", self.temp_output.name)
        with open(self.temp_output.name, "r") as f:
            content = f.read()
            self.assertEqual(self.expected, content)

    def test_convert_files(self):
        """Should convert document into a specified format using django files"""
        output = convert_file(self.temp_input, "md")
        with open(os.path.join(settings.MEDIA_ROOT, output.name), "r") as f:
            content = f.read()
            self.assertEqual(self.expected, content)
