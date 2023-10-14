from rest_framework.serializers import ModelSerializer, ValidationError

from api.v1.upload.serializers import UploadSerializer
from task.models import OCRTask
from upload.models import Upload


class CreateOCRTaskSerializer(ModelSerializer):
    class Meta:
        model = OCRTask
        fields = [
            "name",
            "upload",
            "language",
        ]

    def validate(self, attrs):
        if attrs.get("upload").media_type != Upload.MediaTypes.IMAGE:
            raise ValidationError("Uploaded file is not an image")
        return attrs


class OCRTaskSerializer(ModelSerializer):
    upload = UploadSerializer()

    class Meta:
        model = OCRTask
        fields = [
            "id",
            "name",
            "status",
            "created_at",
            "closed_at",
            "upload",
            "language",
            "output"
        ]
