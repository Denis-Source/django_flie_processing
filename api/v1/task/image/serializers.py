from pathlib import Path

from django.core.validators import MaxValueValidator
from rest_framework import serializers
from rest_framework.fields import IntegerField
from rest_framework.serializers import ModelSerializer

from task.image.constants import INPUT_FORMATS
from task.models import ImageConversionTask


class ImageConversionTaskSerializer(ModelSerializer):
    quality = IntegerField(
        default=100,
        min_value=1,
        max_value=100,
    )

    class Meta:
        model = ImageConversionTask
        fields = [
            "id",
            "name",
            "status",
            "created_at",
            "closed_at",
            "output_format",
            "input_file",
            "output_file",
            "quality",
        ]
        read_only_fields = (
            "id",
            "status",
            "created_at",
            "closed_at",
            "output_file",
        )

    def validate_input_file(self, value):
        file_extension = Path(value.name).suffix[1:].lower()
        allowed_formats = [f for f, _ in INPUT_FORMATS.items()]
        if not file_extension in allowed_formats:
            allowed_formats_str = ", ".join(allowed_formats)
            raise serializers.ValidationError(f"Unsupported file format. Allowed formats are: {allowed_formats_str}.")

        return value