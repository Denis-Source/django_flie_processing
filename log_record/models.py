from django.db import models


class LogRecord(models.Model):
    class LogLevels(models.IntegerChoices):
        NOT_SET = 0, "NOT SET"
        DEBUG = 10, "DEBUG"
        INFO = 20, "INFO"
        WARNING = 30, "WARNING"
        ERROR = 40, "ERROR"
        CRITICAL = 50, "CRITICAL"

    name = models.CharField(max_length=64, verbose_name="Record name", editable=False)
    level = models.IntegerField(choices=LogLevels.choices, verbose_name="Log level", editable=False)
    message = models.CharField(max_length=256, blank=True, null=True, editable=False)
    timedate = models.DateTimeField(auto_now_add=True, verbose_name="Creation date", editable=False)

    def __str__(self):
        return f"{self.name} {self.level} {self.message}"