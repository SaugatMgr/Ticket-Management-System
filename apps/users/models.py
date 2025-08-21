import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from utils.models import BaseModel


class Permission(BaseModel):
    """
    Represents a permission that can be assigned to roles.
    """

    codename = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.codename


class Role(BaseModel):
    """
    Represents a user role that can be assigned to users.
    """

    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    """
    Represents a user in the system.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_menus = models.ManyToManyField(
        "tickets.MenuLevel3", blank=True, related_name="assigned_users"
    )
    created_at = models.DateTimeField("created at", auto_now_add=True, null=True)
    modified_at = models.DateTimeField("last modified at", auto_now=True, null=True)

    def has_permission(self, codename):
        """Check if user's role has given permission"""
        if not self.role:
            return False
        return self.role.permissions.filter(codename=codename).exists()
