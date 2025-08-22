from rest_framework.routers import DefaultRouter

from apps.users.api.v1.views.viewsets import PermissionViewSet, RoleViewSet

user_router = DefaultRouter()


user_router.register(r"roles", RoleViewSet, basename="role")
user_router.register(r"permissions", PermissionViewSet, basename="permission")
