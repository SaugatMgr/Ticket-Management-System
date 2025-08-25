from django.contrib import admin

from apps.notifications.models import NotificationLog


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "action",
        "message",
        "content_type",
        "object_id",
        "created_at",
    )
    list_filter = ("action", "content_type", "created_at")
    search_fields = ("user__email", "user__username", "message", "object_id")
    readonly_fields = (
        "user",
        "action",
        "message",
        "content_type",
        "object_id",
        "content_object",
        "created_at",
    )
    ordering = ("-created_at",)

    # Disable manual add/edit/delete
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
