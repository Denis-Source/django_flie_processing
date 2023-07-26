from django.core.validators import RegexValidator
from rest_framework import serializers
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


class TaskCreateSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "name"
        ]
