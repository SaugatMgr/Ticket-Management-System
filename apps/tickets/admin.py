from django.contrib import admin

from .models import (
    MenuLevel1,
    MenuLevel2,
    MenuLevel3,
    Ticket,
    TicketPriority,
    TicketStatus,
)


@admin.register(TicketStatus)
class TicketStatusAdmin(admin.ModelAdmin):
    """Admin panel for TicketStatus."""

    list_display = ("name", "created_at", "modified_at", "created_by", "modified_by")
    search_fields = ("name",)
    list_filter = ("created_at",)
    ordering = ("name",)

    readonly_fields = ("created_at", "modified_at", "created_by", "modified_by")


@admin.register(TicketPriority)
class TicketPriorityAdmin(admin.ModelAdmin):
    """Admin panel for TicketPriority."""

    list_display = (
        "name",
        "weight",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
    )
    search_fields = ("name",)
    list_filter = ("weight", "created_at")
    ordering = ("weight",)

    readonly_fields = ("created_at", "modified_at", "created_by", "modified_by")


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """Admin panel for Ticket."""

    list_display = (
        "title",
        "status",
        "priority",
        "assigned_to",
        "created_by",
        "created_at",
    )
    list_filter = ("status", "priority", "assigned_to", "created_at")
    search_fields = ("title", "description")
    ordering = ("-created_at",)

    readonly_fields = ("created_at", "modified_at", "created_by", "modified_by")

    autocomplete_fields = ("status", "priority", "assigned_to")


@admin.register(MenuLevel1)
class MenuLevel1Admin(admin.ModelAdmin):
    list_display = ("name", "created_by", "created_at")
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ("created_at", "modified_at", "created_by", "modified_by")


@admin.register(MenuLevel2)
class MenuLevel2Admin(admin.ModelAdmin):
    list_display = ("name", "parent", "created_by", "created_at")
    search_fields = ("name", "parent__name")
    list_filter = ("parent",)
    ordering = ("parent__name", "name")
    readonly_fields = ("created_at", "modified_at", "created_by", "modified_by")

    autocomplete_fields = ("parent",)


@admin.register(MenuLevel3)
class MenuLevel3Admin(admin.ModelAdmin):
    list_display = ("name", "parent", "created_by", "created_at")
    search_fields = ("name", "parent__name", "parent__parent__name")
    list_filter = ("parent__parent", "parent")
    ordering = ("parent__parent__name", "parent__name", "name")
    readonly_fields = ("created_at", "modified_at", "created_by", "modified_by")

    autocomplete_fields = ("parent",)
