from datetime import timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from clipboard.models import ClipBoard
from core import settings
from user.models import User


class TaskClipboardCase(TestCase):
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

    def generate_clipboard_sample(self, n):
        for i in range(n):
            clipboard = ClipBoard(
                name="test",
                media_type=ClipBoard.MediaTypes.DOCUMENT,
                file=self.file,
                auto_delete=i % 2 == 0,
                user=self.user if i % 2 == 0 else self.other_user
            )
            clipboard.save()

    def test_stale_clipboards(self):
        clipboard = ClipBoard(
            name="test",
            media_type=ClipBoard.MediaTypes.DOCUMENT,
            file=self.file,
            auto_delete=True,
            user=self.user,
            created_at=timezone.now() - timedelta(days=settings.CLIPBOARD_MEDIA_AGE + 10)
        )
        clipboard.save()
        stale_clipboards = ClipBoard.get_stale_clipboards()
        self.assertEqual(len(stale_clipboards), 1)
        self.assertIn(clipboard, stale_clipboards)

    def test_user_clipboards(self):
        self.generate_clipboard_sample(self.n)
        expected_amount = self.n // 2
        self.assertTrue(self.n % 2 == 0)
        self.assertEqual(expected_amount, len(ClipBoard.get_users_clipboard(self.user)))
        self.assertEqual(expected_amount, len(ClipBoard.objects.filter(user=self.user)))