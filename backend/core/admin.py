# core/admin.py
from django.contrib import admin

from .models import Log
from .models import Notification
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin[Service]):
    list_display = (
        "id",
        "name",
        "url",
        "is_paused",
        "data_created",
    )
    list_filter = ("name",)
    search_fields = ("name", "url")


@admin.register(Log)
class LogAdmin(admin.ModelAdmin[Log]):
    list_display = (
        "id",
        "service",
        "status_badge",
        "last_checked",
        "status_code",
    )
    list_filter = ("service", "is_up")
    search_fields = ("service", "status_code")

    list_per_page = 20

    def status_badge(self, obj: Log):
        if obj.is_up is True:
            return "🟢 Up"
        elif obj.is_up is False:
            return "🔴 Down"
        return "⚪ Unknown"


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin[Log]):
    list_display = (
        "id",
        "service",
        "webhook_url",
    )
    list_filter = ("service",)
    search_fields = ("service",)
