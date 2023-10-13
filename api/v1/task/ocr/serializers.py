from rest_framework.serializers import ModelSerializer

from api.v1.upload.serializers import UploadSerializer
from task.models import OCRTask


class CreateOCRTaskSerializer(ModelSerializer):
    class Meta:
        model = OCRTask
        fields = [
            "name",
            "upload",
            "language",
        ]

class OCRTaskSerializer(ModelSerializer):
    upload = UploadSerializer()

    class Meta:
        model = OCRTask
        fields = [
            "name",
            "status",
            "created_at",
            "closed_at",
            "upload",
            "language",
            "output"
        ]
