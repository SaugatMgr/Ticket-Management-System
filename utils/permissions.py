# This file contains custom permissions for the API.

from rest_framework.permissions import BasePermission


class RolePermission(BasePermission):
    """
    Checks if the user's role has permission for the current action.
    """

    perms_map = {
        "create": "can_create_{model}",
        "list": "can_view_{model}",
        "retrieve": "can_view_{model}",
        "update": "can_edit_{model}",
        "partial_update": "can_edit_{model}",
        "destroy": "can_delete_{model}",
    }

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        action = getattr(view, "action", None)
        model_name = view.queryset.model._meta.model_name

        required_perm = self.perms_map.get(action, "").format(model=model_name)

        if not required_perm:
            return False

        return user.has_permission(required_perm)


class IsAdmin(BasePermission):
    message = "Only Admin can access"

    def has_permission(self, request, view):
        user = request.user
        user_is_active_and_authenticated = user.is_active and user.is_authenticated

        if not user_is_active_and_authenticated:
            return False
        if user.is_superuser:
            return True
        return user.role.name.lower() == "admin"
