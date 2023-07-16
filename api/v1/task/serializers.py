from rest_framework.serializers import ModelSerializer

from task.models import Task, MazeGenerationTask


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


class TaskCreateSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "name"
        ]


class MazeCreationTaskGenerationSerializer(ModelSerializer):
    class Meta:
        model = MazeGenerationTask
        fields = [
            "name",
            "width",
            "height",
            "algorithm"
        ]
