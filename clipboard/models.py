from django.db import models
from django.utils import timezone

from core import settings
from core.constants import IMAGE_INPUT_FORMATS, VIDEO_INPUT_FORMATS, DOCUMENT_INPUT_FORMATS
from user.models import User


class ClipBoard(models.Model):
    FOLDER = "clipboards"

    class MediaTypes(models.TextChoices):
        IMAGE = "image", "Image"
        VIDEO = "video", "Video"
        DOCUMENT = "document", "Document"
        OTHER = "other", "Other"

    name = models.CharField(
        max_length=256,
        verbose_name="Name", help_text="Name of the clipboard"
    )
    media_type = models.CharField(
        max_length=10, default=MediaTypes.OTHER, choices=MediaTypes.choices,
        verbose_name="Media type", help_text="Media type of the clipboard file"
    )
    file = models.FileField(
        upload_to=FOLDER,
        verbose_name="Media file", help_text="Media file"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Creation date",
        help_text="Date the clipboard was created at"
    )
    auto_delete = models.BooleanField(
        default=True,
        verbose_name="Auto delete flag",
        help_text="Whether the media will be deleted after some time"
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        verbose_name="User", help_text="User that uploaded a clipboard"
    )

    def __str__(self):
        return f"{self.user} {self.media_type} {self.name}"

    def save(self, *args, **kwargs):
        if not self.media_type:
            self.media_type = self.get_media_type(self.file.name)
        super().save(*args, **kwargs)

    @classmethod
    def get_stale_clipboards(cls):
        """Get clipboard instances that are considered stale"""
        cutoff_time = timezone.now() - timezone.timedelta(days=settings.CLIPBOARD_MEDIA_AGE)
        return cls.objects.filter(created_at__lte=cutoff_time, auto_delete=True)

    @classmethod
    def get_users_clipboard(cls, user: User):
        """Get clipboard instances that are created by a specified user"""
        return cls.objects.filter(user=user)

    @staticmethod
    def get_media_type(file_name: str) -> str:
        media_types = {
            ClipBoard.MediaTypes.IMAGE: IMAGE_INPUT_FORMATS,
            ClipBoard.MediaTypes.VIDEO: VIDEO_INPUT_FORMATS,
            ClipBoard.MediaTypes.DOCUMENT: DOCUMENT_INPUT_FORMATS,
        }
        media_format = file_name.split(".")[-1]

        for media_type, formats in media_types.items():
            if media_format in formats:
                return media_type

        return ClipBoard.MediaTypes.OTHER
