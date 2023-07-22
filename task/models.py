from django.db import models
from django.utils import timezone

from core import settings
from task.maze.maze import BINARY_TREE, SIDEWINDER, ALDOUS_BRODER, WILSON, HUNT_AND_KILL, RECURSIVE_BACKTRACKER
from user.models import User


class Task(models.Model):
    class Meta:
        ordering = ["created_at"]

    class Statuses(models.TextChoices):
        CREATED = "created"
        RUNNING = "running"
        FINISHED = "finished"
        ERRORED = "errored"
        CANCELED = "canceled"

    name = models.CharField(
        max_length=64, verbose_name="Name", help_text="Name of the task")
    status = models.CharField(
        max_length=10, default=Statuses.CREATED, choices=Statuses.choices,
        verbose_name="Status", help_text="Current state of the task")
    created_at = models.DateTimeField(
        editable=False, verbose_name="Creation date",
        help_text="Date that the task was create")
    closed_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Closure date",
        help_text="Date that the task was finished/errored")
    initiator = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Task initiator",
        help_text="User that initiated the task")

    def __str__(self):
        return f"{self.status} {self.name}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super().save(*args, **kwargs)

    def update_status(self, new_status):
        if new_status in dict(self.Statuses.choices):
            self.status = new_status
            if new_status in [self.Statuses.FINISHED, self.Statuses.ERRORED, self.Statuses.CANCELED]:
                self.closed_at = timezone.now()
            self.save()
        else:
            raise ValueError("Invalid status value")

    @classmethod
    def get_stale_tasks(cls):
        cutoff_time = timezone.now() - timezone.timedelta(seconds=settings.STALE_TASK_AGE)
        return cls.objects.filter(created_at__lte=cutoff_time, status__in=[cls.Statuses.CREATED, cls.Statuses.RUNNING])

    @classmethod
    def get_opened_tasks(cls):
        return cls.objects.filter(status__in=[cls.Statuses.CREATED, cls.Statuses.RUNNING])

    @classmethod
    def get_closed_tasks(cls):
        return cls.objects.filter(status__in=[cls.Statuses.ERRORED, cls.Statuses.FINISHED, cls.Statuses.CANCELED])


class MazeGenerationTask(Task):
    class ALGORITHMS(models.TextChoices):
        BINARY_TREE = BINARY_TREE
        SIDEWINDER = SIDEWINDER
        ALDOUS_BRODER = ALDOUS_BRODER
        WILSON = WILSON
        HUNT_AND_KILL = HUNT_AND_KILL
        RECURSIVE_BACKTRACKER = RECURSIVE_BACKTRACKER

    columns = models.IntegerField(
        default=75,
        verbose_name="Columns", help_text="Number of cells in a column")
    rows = models.IntegerField(
        default=75,
        verbose_name="Rows", help_text="Number of cells in a row")
    scale = models.IntegerField(
        default=4,
        verbose_name="Scale", help_text="Number of pixels per cell")
    algorithm = models.CharField(
        max_length=32, default=ALGORITHMS.BINARY_TREE, choices=ALGORITHMS.choices,
        verbose_name="Generation algorithm", help_text="Algorithm used for maze generation")
    result = models.ImageField(
        upload_to="mazes", blank=True, null=True,
        verbose_name="Result Image", help_text="Result Image")

    def set_result(self, result):
        self.result = result
        self.save()
