from django.apps import AppConfig


class LogStreamConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.v1.log_stream"

    def ready(self):
        from . import signals
        return super().ready()