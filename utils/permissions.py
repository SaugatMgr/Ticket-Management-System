# This file contains custom permissions for the API.

from rest_framework.permissions import BasePermission


class HasPermission(BasePermission):
    """
    Generic permission check against user's role permissions.
    """

    required_permission: str = None

    def has_permission(self, request, view):
        if not self.required_permission:
            return True  # If no specific permission is required, allow access

        return request.user.is_authenticated and request.user.has_permission(
            self.required_permission
        )


class CanManageTicket(HasPermission):
    required_permission = "can_manage_ticket"


class CanManageTicketStatus(HasPermission):
    required_permission = "can_manage_ticket_status"


class CanManageTicketPriority(HasPermission):
    required_permission = "can_manage_ticket_priority"
