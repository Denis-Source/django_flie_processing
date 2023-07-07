from django.contrib import admin

from log_record.models import LogRecord


@admin.register(LogRecord)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "timedate", "name", "level", "message")
    list_filter = ("level",)
    search_fields = ("id", "timedate", "name", "level")
    ordering = ("timedate",)
