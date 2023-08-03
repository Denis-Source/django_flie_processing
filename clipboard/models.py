from datetime import timezone

from django.db import models

from user.models import User


class ClipBoard(models.Model):
    FOLDER = "clipboards"

    class MediaTypes(models.TextChoices):
        IMAGE = "image"
        VIDEO = "video"
        DOCUMENT = "document"
        OTHER = "other"

    name = models.CharField(
        max_length=32, unique=True,
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
        null=True, blank=True,
        verbose_name="Creation date",
        help_text="Date the clipboard was created at"
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        verbose_name="User", help_text="User that uploaded a clipboard"
    )

    def __str__(self):
        return f"{self.user} {self.media_type} {self.name}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super().save(*args, **kwargs)
