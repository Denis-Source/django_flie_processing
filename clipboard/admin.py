from django.contrib import admin

from clipboard.models import ClipBoard


@admin.register(ClipBoard)
class ClipboardAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "media_type", "created_at", "user")
    list_filter = ("media_type", "user")
    search_fields = ("id", "name", "user")
    ordering = ("-created_at",)