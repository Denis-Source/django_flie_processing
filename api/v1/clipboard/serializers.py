from urllib.parse import urljoin

from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError

from clipboard.models import ClipBoard
from core import settings


class ClipBoardSerializer(ModelSerializer):
    file_size = SerializerMethodField(method_name="get_file_size")
    file_url = SerializerMethodField(method_name="get_file_url")

    class Meta:
        model = ClipBoard
        fields = [
            "id",
            "name",
            "media_type",
            "file",
            "file_url",
            "file_size",
            "created_at",
            "auto_delete"
        ]
        read_only_fields = (
            "id",
            "created_at",
            "file_size",
        )
        write_only_fields = (
            "file"
        )

    def validate_file(self, value):
        if value.size > settings.MAX_FILE_UPLOAD_SIZE:
            raise ValidationError("FIle size exceeded")
        return value

    def get_file_size(self, obj):
        return obj.file.size

    def get_file_url(self, obj):
        return urljoin(settings.HOST, obj.file.url)
