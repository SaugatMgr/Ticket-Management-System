from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, Permission, Role


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin panel configuration for CustomUser."""

    model = CustomUser

    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "created_at",
    )
    list_filter = ("is_active", "is_staff", "is_superuser", "created_at")
    search_fields = ("email", "username", "first_name", "last_name", "phone")
    ordering = ("-created_at",)

    readonly_fields = (
        "created_at",
        "modified_at",
    )

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "created_at", "modified_at")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Admin panel for Role."""

    list_display = ("name", "created_at", "modified_at", "created_by", "modified_by")
    search_fields = ("name",)
    list_filter = ("created_at",)
    ordering = ("name",)

    readonly_fields = ("created_at", "modified_at", "created_by", "modified_by")


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """Admin panel for custom Permission."""

    list_display = (
        "codename",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
    )
    search_fields = ("codename",)
    list_filter = ("created_at",)
    ordering = ("codename",)

    readonly_fields = ("created_at", "modified_at", "created_by", "modified_by")
