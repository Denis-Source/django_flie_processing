from django.db import models
from django.utils import timezone

from core import settings
from user.models import User


class ClipBoard(models.Model):
    FOLDER = "clipboards"

    class MediaTypes(models.TextChoices):
        IMAGE = "image", "Image"
        VIDEO = "video", "Video"
        DOCUMENT = "document", "Document"
        OTHER = "other", "Other"

    name = models.CharField(
        max_length=32,
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

    @classmethod
    def get_stale_clipboards(cls):
        cutoff_time = timezone.now() - timezone.timedelta(days=settings.CLIPBOARD_MEDIA_AGE)
        return cls.objects.filter(created_at__lte=cutoff_time, auto_delete=True)

    @classmethod
    def get_users_clipboard(cls, user: User):
        return cls.objects.filter(user=user)
