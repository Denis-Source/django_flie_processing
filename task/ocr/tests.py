from django.test import TestCase

from core import settings
from task.ocr.data.transacriptions import UKR_TRANSCRIPTION, ENG_TEST_IMAGE, UKR_TEST_IMAGE, \
    TRANSCRIPTIONS
from task.ocr.services import get_text_from_path
from upload.models import Upload


class OCRTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.test_image_path = settings.BASE_DIR.joinpath("task/ocr/data/image.jpg")
        self.upload = Upload.objects.create()

    def test_image_path_default_success(self):
        image_path = ENG_TEST_IMAGE

        result = get_text_from_path(settings.BASE_DIR.joinpath(image_path))
        self.assertEqual(
            TRANSCRIPTIONS[image_path],
            result
        )

    def test_image_path_ukr_success(self):
        image_path = UKR_TEST_IMAGE

        result = get_text_from_path(settings.BASE_DIR.joinpath(image_path), languages=["ukr"])
        expected = UKR_TRANSCRIPTION
        self.assertEqual(
            TRANSCRIPTIONS[image_path],
            result
        )
