from rest_framework.serializers import ModelSerializer

from task.models import Task


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
