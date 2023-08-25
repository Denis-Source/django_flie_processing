from django.contrib import admin

from upload.models import Upload


@admin.register(Upload)
class ClipboardAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "media_type", "created_at", "user")
    list_filter = ("media_type", "user")
    search_fields = ("id", "name", "user")
    ordering = ("-created_at",)
