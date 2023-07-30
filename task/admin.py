from django.contrib import admin

from task.models import Task, ConversionTask, DocumentConversionTask, ImageConversionTask


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "name", "created_at", "closed_at")
    list_filter = ("status",)
    search_fields = ("id", "status", "name", "created_at", "closed_at")
    ordering = ("-created_at",)


@admin.register(ConversionTask)
class ConversionTaskAdmin(TaskAdmin):
    pass


@admin.register(DocumentConversionTask)
class DocumentConversionTaskAdmin(TaskAdmin):
    list_display = ("id", "status", "name", "created_at", "closed_at", "output_format")
    list_filter = ("status", "output_format")


@admin.register(ImageConversionTask)
class ImageConversionTaskAdmin(TaskAdmin):
    list_display = ("id", "status", "name", "created_at", "closed_at", "output_format", "quality")
    list_filter = ("status", "output_format")
