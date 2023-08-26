from urllib.parse import urljoin

from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from rest_framework.serializers import IntegerField, ValidationError
from rest_framework.serializers import ModelSerializer

from api.v1.upload.serializers import UploadSerializer
from core import settings
from core.constants import IMAGE_OUTPUT_FORMATS, DOCUMENT_OUTPUT_FORMATS
from task.models import Task, ConversionTask
from upload.models import Upload


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "status",
            "created_at",
            "closed_at"
        ]

class CreateConversionTaskSerializer(ModelSerializer):
    quality = IntegerField(
        default=100,
        min_value=1,
        max_value=100,
        required=False
    )
    class Meta:
        model = ConversionTask
        fields = [
            "name",
            "output_format",
            "upload",
            "quality"
        ]

class ConversionTaskSerializer(ModelSerializer):
    upload = UploadSerializer()
    output_file = SerializerMethodField(method_name="get_output_file")
    output_file_size = SerializerMethodField(method_name="get_output_file_size")

    def get_output_file(self, obj):
        if obj.output_file:
            return urljoin(settings.HOST, obj.output_file.url)

    def get_output_file_size(self, obj):
        if obj.output_file:
            return obj.output_file.size
        else:
            return None

    class Meta:
        model = ConversionTask
        fields = [
            "id",
            "name",
            "status",
            "created_at",
            "closed_at",
            "output_format",
            "upload",
            "output_file",
            "output_file_size",
            "quality",
        ]
        read_only_fields = (
            "id",
            "status",
            "created_at",
            "closed_at",
            "output_file",
        )

    def validate(self, data):
        upload = data["upload"]
        output_format = data["output_format"]

        match data["upload"].media_type:
            case Upload.MediaTypes.IMAGE:
                if not output_format in IMAGE_OUTPUT_FORMATS:
                    raise ValidationError(f"Output format {output_format} is wrong for media type {upload.media_type}")
            case Upload.MediaTypes.DOCUMENT:
                if not output_format in DOCUMENT_OUTPUT_FORMATS:
                    raise ValidationError(f"Output format {output_format} is wrong for {upload.media_type}")
        return data

    def validate_upload(self, upload: Upload):
        if upload.media_type not in [Upload.MediaTypes.IMAGE, Upload.MediaTypes.DOCUMENT]:
            raise ValidationError("Provided format is not supported")

        return upload
