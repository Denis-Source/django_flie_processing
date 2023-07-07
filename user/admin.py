from django.contrib import admin

from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "username", "role")
    list_filter = ("role",)
    search_fields = ("id", "email", "username")
    ordering = ("registered",)
