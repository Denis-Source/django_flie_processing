from django.core.validators import RegexValidator
from rest_framework import serializers
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


class MazeCreationGenerationTaskSerializer(ModelSerializer):
    name = serializers.CharField(
        min_length=3,
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9_]+$",
                message="Name can only contain alphanumeric characters and underscores")])
    columns = serializers.IntegerField(min_value=2, max_value=200)
    rows = serializers.IntegerField(min_value=2, max_value=200)
    scale = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = MazeGenerationTask
        fields = [
            "name",
            "rows",
            "columns",
            "scale",
            "algorithm"
        ]
