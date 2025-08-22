from rest_framework import permissions, viewsets

from apps.users.api.v1.serializers.serializers import (
    CreateRoleSerializer,
    PermissionSerializer,
    RoleSerializer,
)
from apps.users.models import Permission, Role
from utils.pagination import CustomPageSizePagination


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = CustomPageSizePagination
    search_fields = ["codename"]
    filterset_fields = ["codename"]
    ordering_fields = ["codename"]


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.prefetch_related("permissions")
    pagination_class = CustomPageSizePagination
    search_fields = ["name", "permissions__codename"]
    filterset_fields = ["name", "permissions"]
    ordering_fields = ["name", "permissions__codename"]

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return CreateRoleSerializer
        return RoleSerializer
