from rest_framework.serializers import ModelSerializer

from log_record.models import LogRecord


class LogStreamSerializer(ModelSerializer):
    class Meta:
        model = LogRecord
        fields = [
            "id",
            "name",
            "level",
            "message",
            "timedate"
        ]
