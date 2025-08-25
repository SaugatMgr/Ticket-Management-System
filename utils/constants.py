# This file contains constants for all models.

from django.db.models import TextChoices


class NotificationLogActionChoices(TextChoices):
    CREATE = "create", "Created"
    UPDATE = "update", "Updated"
    DELETE = "delete", "Deleted"
    ASSIGN = "assign", "Assigned"
    UNASSIGN = "unassign", "Unassigned"
    REASSIGN = "reassign", "Reassigned"
