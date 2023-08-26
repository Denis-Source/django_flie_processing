from django.db import models
from django.utils import timezone
from uuid import uuid4

from core import settings
from core.constants import IMAGE_INPUT_FORMATS, VIDEO_INPUT_FORMATS, DOCUMENT_INPUT_FORMATS
from user.models import User


class Upload(models.Model):
    FOLDER = "uploads"

    class MediaTypes(models.TextChoices):
        IMAGE = "image", "Image"
        VIDEO = "video", "Video"
        DOCUMENT = "document", "Document"
        OTHER = "other", "Other"

    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False)

    name = models.CharField(
        max_length=256,
        verbose_name="Name", help_text="Name of the upload"
    )
    media_type = models.CharField(
        max_length=10, default=MediaTypes.OTHER, editable=False, choices=MediaTypes.choices,
        verbose_name="Media type", help_text="Media type of the upload file"
    )
    file = models.FileField(
        upload_to=FOLDER,
        verbose_name="Media file", help_text="Media file"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Creation date",
        help_text="Date the upload was created at"
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        verbose_name="User", help_text="User that uploaded a upload"
    )

    def __str__(self):
        return f"{self.user} {self.media_type} {self.name}"

    def save(self, *args, **kwargs):
        self.media_type = self.get_media_type(self.file.name)
        super().save(*args, **kwargs)

    @classmethod
    def get_users_uploads(cls, user: User):
        """Get upload instances that are created by a specified user"""
        return cls.objects.filter(user=user).order_by("-created_at")

    @staticmethod
    def get_media_type(file_name: str) -> str:
        media_types = {
            Upload.MediaTypes.IMAGE: IMAGE_INPUT_FORMATS,
            Upload.MediaTypes.VIDEO: VIDEO_INPUT_FORMATS,
            Upload.MediaTypes.DOCUMENT: DOCUMENT_INPUT_FORMATS,
        }
        media_format = file_name.split(".")[-1].lower()

        for media_type, formats in media_types.items():
            if media_format in formats:
                return media_type

        return Upload.MediaTypes.OTHER
