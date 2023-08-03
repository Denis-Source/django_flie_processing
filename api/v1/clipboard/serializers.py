from rest_framework.serializers import ModelSerializer, SerializerMethodField

from clipboard.models import ClipBoard


class ClipBoardSerializer(ModelSerializer):
    file_size = SerializerMethodField(method_name="get_file_size")

    class Meta:
        model = ClipBoard
        fields = [
            "id",
            "name",
            "media_type",
            "file",
            "file_size",
            "created_at",
            "auto_delete"
        ]
        read_only_fields = (
            "id",
            "created_at",
            "file_size"
        )

    def get_file_size(self, obj):
        return obj.file.size
