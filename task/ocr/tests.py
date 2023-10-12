from django.test import TestCase

from core import settings
from task.ocr.data.transacriptions import ENG_TRANSCRIPTION, UKR_TRANSCRIPTION
from task.ocr.services import get_text_from_image


class OCRTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.test_image_path = settings.BASE_DIR.joinpath("task/ocr/data/image.jpg")

    def test_image_default_success(self):
        result = get_text_from_image(self.test_image_path)
        self.assertEqual(
            ENG_TRANSCRIPTION,
            result
        )

    def test_image_ukr_success(self):
        result = get_text_from_image(settings.BASE_DIR.joinpath("task/ocr/data/ukr.png"), languages=["ukr"])
        expected = UKR_TRANSCRIPTION
        self.assertEqual(
            UKR_TRANSCRIPTION,
            result
        )