import os
from random import randint
from tempfile import NamedTemporaryFile

from PIL import Image
from django.test import TestCase

from task.image.constants import COLOR_MODES
from task.image.serivces import convert_path, convert_file

def generate_noisy_image(image,  noise_intensity=30):
    width, height = image.size
    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            noise_r = randint(-noise_intensity, noise_intensity)
            noise_g = randint(-noise_intensity, noise_intensity)
            noise_b = randint(-noise_intensity, noise_intensity)

            r = max(0, min(255, r + noise_r))
            g = max(0, min(255, g + noise_g))
            b = max(0, min(255, b + noise_b))
            image.putpixel((x, y), (r, g, b))
    return image

class ImageTestCase(TestCase):
    def setUp(self) -> None:
        self.input_suffix = "png"
        self.another_output_suffix = "msp"
        self.output_suffix = "jpeg"

        self.size = 100, 100

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
        convert_path(self.temp_input.name, self.temp_output.name)
        width, height = self.size
        result_image = Image.open(self.temp_output.name)
        self.assertTrue(result_image)

    def test_convert_paths_wrong_color_mode(self):
        convert_path(self.temp_input.name, self.another_temp_output.name)
        result_image = Image.open(self.another_temp_output.name)
        self.assertTrue(result_image)

        self.assertNotEqual(self.image.mode, COLOR_MODES[self.another_output_suffix])
        self.assertNotEqual(self.image.mode, result_image.mode)
        self.assertEqual(result_image.mode, COLOR_MODES[self.another_output_suffix])

    def test_convert_files(self):
        output = convert_file(self.temp_input, "md", self.temp_output)
        result_image = Image.open(self.temp_output.name)
        self.assertTrue(result_image)