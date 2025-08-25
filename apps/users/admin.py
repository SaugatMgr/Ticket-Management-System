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
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
        "created_at",
    )
    list_filter = ("role", "is_active", "is_staff", "is_superuser", "created_at")
    search_fields = (
        "email",
        "username",
        "first_name",
        "last_name",
        "phone",
        "role__name",
    )
    ordering = ("-created_at",)
    filter_horizontal = ()

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
                    "role",
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
                    "role",
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

    list_display = ("codename",)
    search_fields = ("codename",)
    ordering = ("codename",)
