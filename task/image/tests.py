import os
from tempfile import NamedTemporaryFile

from PIL import Image
from django.test import TestCase

from core import settings
from core.constants import IMAGE_OUTPUT_FORMATS, IMAGE_INPUT_FORMATS
from task.image.constants import COLOR_MODES
from task.image.serivces import convert_path, convert_file
from utils.generation import generate_noisy_image


class ImageTestCase(TestCase):
    def setUp(self) -> None:
        self.input_suffix = "png"
        self.another_output_suffix = "msp"
        self.output_suffix = "jpeg"

        self.size = 50, 50

        self.image = Image.new("RGB", self.size, "white")
        self.image = generate_noisy_image(self.image)

        self.temp_input = NamedTemporaryFile(delete=False, suffix=f".{self.input_suffix}")
        self.temp_input.close()
        self.image.save(self.temp_input.name)

        self.temp_output = NamedTemporaryFile(delete=False, suffix=f".{self.output_suffix}")
        self.temp_output.close()

        self.another_temp_output = NamedTemporaryFile(delete=False, suffix=f".{self.another_output_suffix}")
        self.another_temp_output.close()

    def tearDown(self):
        super().tearDown()
        os.remove(self.temp_input.name)
        os.remove(self.temp_output.name)
        os.remove(self.another_temp_output.name)

    def test_convert_paths(self):
        """Should convert image into a specified format using paths"""
        convert_path(self.temp_input.name, self.temp_output.name)
        width, height = self.size
        result_image = Image.open(self.temp_output.name)
        self.assertTrue(result_image)

    def test_convert_paths_wrong_color_mode(self):
        """Should change image color mode if needed"""
        convert_path(self.temp_input.name, self.another_temp_output.name)
        result_image = Image.open(self.another_temp_output.name)
        self.assertTrue(result_image)

        self.assertNotEqual(self.image.mode, COLOR_MODES[self.another_output_suffix])
        self.assertNotEqual(self.image.mode, result_image.mode)
        self.assertEqual(result_image.mode, COLOR_MODES[self.another_output_suffix])

    def test_convert_formats(self):
        """Should convert images for all available combination of input-output formats"""
        for input_format in IMAGE_INPUT_FORMATS.keys():
            for output_format in IMAGE_OUTPUT_FORMATS.keys():
                image = Image.new(COLOR_MODES[input_format], self.size, "white")
                image = generate_noisy_image(image)
                temp_input = NamedTemporaryFile(delete=False, suffix=f".{input_format}")
                image.save(temp_input.name)
                output = None
                try:
                    output = convert_file(temp_input, output_format)
                    result_image = Image.open(os.path.join(settings.MEDIA_ROOT, output.name))
                    self.assertTrue(result_image)
                except Exception as e:
                    self.fail(e)
                finally:
                    if output:
                        os.remove(os.path.join(settings.MEDIA_ROOT, output.name))