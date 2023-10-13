from django.apps import AppConfig


class TaskConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.v1.task.conversion"
    label = "api_v1_task_conversion"

    def ready(self):
        from . import signals
