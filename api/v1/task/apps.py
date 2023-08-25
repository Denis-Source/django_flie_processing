from django.apps import AppConfig


class TaskConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.v1.task"
    label = "api_v1_task"

    def ready(self):
        from . import signals