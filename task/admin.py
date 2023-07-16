from django.contrib import admin

from task.models import Task, MazeGenerationTask


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "name", "created_at", "closed_at")
    list_filter = ("status",)
    search_fields = ("id", "status", "name", "created_at", "closed_at")
    ordering = ("-created_at",)


@admin.register(MazeGenerationTask)
class MazeGenerationTaskAdmin(TaskAdmin):
    pass
