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


class MazeCreationTaskGenerationSerializer(ModelSerializer):
    width = serializers.IntegerField(min_value=10, max_value=150)
    height = serializers.IntegerField(min_value=10, max_value=150)
    name = serializers.CharField(
        min_length=3,
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9_]+$",
                message="Name can only contain alphanumeric characters and underscores.")])

    class Meta:
        model = MazeGenerationTask
        fields = [
            "name",
            "width",
            "height",
            "algorithm"
        ]
