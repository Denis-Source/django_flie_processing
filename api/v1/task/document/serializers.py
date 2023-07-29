from pathlib import Path

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from task.document.constants import INPUT_FORMATS
from task.models import DocumentConversionTask


class DocumentConversionTaskSerializer(ModelSerializer):
    class Meta:
        model = DocumentConversionTask
        fields = [
            "id",
            "name",
            "status",
            "created_at",
            "input_file",
            "output_format",
        ]
        read_only_fields = (
            "id",
            "status",
            "created_at",
        )

    def validate_input_file(self, value):
        file_extension = Path(value.name).suffix[1:].lower()
        allowed_formats = [f for f, _ in INPUT_FORMATS.items()]
        if not file_extension in allowed_formats:
            allowed_formats_str = ", ".join(allowed_formats)
            raise serializers.ValidationError(f"Unsupported file format. Allowed formats are: {allowed_formats_str}.")

        return value
