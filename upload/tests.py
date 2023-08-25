from datetime import timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from upload.models import Upload
from core import settings
from user.models import User


class TaskUploadCase(TestCase):
    def setUp(self):
        self.user = User(
            email="test@mail.com",
            username="cool_test",
        )
        self.other_user = User(
            email="test2@mail.com",
            username="cool_test2"
        )
        self.user.save()
        self.other_user.save()
        self.file = SimpleUploadedFile(
            "testfile.txt",
            b"test content"
        )
        self.n = 100

    def generate_upload_sample(self, n):
        """Generate a sample of uploads that are varied in user"""
        for i in range(n):
            upload = Upload(
                name="test",
                file=self.file,
                user=self.user if i % 2 == 0 else self.other_user
            )
            upload.save()

    def test_user_uploads(self):
        """Should return a list of upload that are created by a specified user"""
        self.generate_upload_sample(self.n)
        expected_amount = self.n // 2
        self.assertTrue(self.n % 2 == 0)
        self.assertEqual(expected_amount, len(Upload.get_users_uploads(self.user)))
        self.assertEqual(expected_amount, len(Upload.objects.filter(user=self.user)))

    def test_get_media_type_image(self):
        file_name = "example.png"
        media_type = Upload.get_media_type(file_name)
        self.assertEqual(media_type, Upload.MediaTypes.IMAGE)

    def test_get_media_type_video(self):
        file_name = "example.mp4"
        media_type = Upload.get_media_type(file_name)
        self.assertEqual(media_type, Upload.MediaTypes.VIDEO)

    def test_get_media_type_document(self):
        file_name = "example.docx"
        media_type = Upload.get_media_type(file_name)
        self.assertEqual(media_type, Upload.MediaTypes.DOCUMENT)

    def test_get_media_type_unknown(self):
        file_name = "example.unknown"
        media_type = Upload.get_media_type(file_name)
        self.assertEqual(media_type, Upload.MediaTypes.OTHER)