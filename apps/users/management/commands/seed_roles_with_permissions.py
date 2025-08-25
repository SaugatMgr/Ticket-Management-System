from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from apps.tickets.models import Ticket, TicketPriority, TicketStatus
from apps.users.models import Role

User = get_user_model()


def get_model_permissions(model, actions=None):
    """
    Return Permission queryset for a given model.
    If actions=None, returns all permissions for that model.
    """
    content_type = ContentType.objects.get_for_model(model)
    qs = Permission.objects.filter(content_type=content_type)
    if actions:
        qs = qs.filter(
            codename__in=[f"{action}{model._meta.model_name}" for action in actions]
        )
    return qs


class Command(BaseCommand):
    help = "Seed roles with permissions and demo users"

    def handle(self, *args, **options):
        role_permissions = {
            "Admin": "_all_",
            "Manager": {
                Ticket: ["add", "view", "change", "delete"],
                TicketStatus: ["add", "view", "change"],
                TicketPriority: ["add", "view", "change"],
            },
            "Support Agent": {
                Ticket: ["view", "change"],
                TicketStatus: ["view"],
                TicketPriority: ["view"],
            },
            "Customer": {
                Ticket: ["add", "view", "change", "delete"],
            },
        }

        roles = {}
        for role_name in role_permissions.keys():
            role, _ = Role.objects.get_or_create(name=role_name)
            roles[role_name] = role

        for role_name, perms_map in role_permissions.items():
            role = roles[role_name]
            if perms_map == "_all_":
                role.permissions.set(Permission.objects.all())
            else:
                perms_qs = Permission.objects.none()
                for model, actions in perms_map.items():
                    perms_qs |= get_model_permissions(model, actions)
                role.permissions.set(perms_qs)
            role.save()
            self.stdout.write(
                self.style.SUCCESS(f"Role {role_name} seeded with permissions")
            )

        demo_users = {
            "admin@gmail.com": ("Admin", "admin"),
            "manager@gmail.com": ("Manager", "manager"),
            "agent@gmail.com": ("Support Agent", "agent"),
            "customer@gmail.com": ("Customer", "customer"),
        }

        for email, (role_name, username) in demo_users.items():
            if not User.objects.filter(email=email).exists():
                demo_password = "test12345"
                user = User.objects.create_user(
                    username=username,
                    email=email,
                )
                user.role = roles[role_name]
                user.set_password(demo_password)
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f"User {email} created with role {role_name}")
                )
            else:
                self.stdout.write(self.style.WARNING(f"User {email} already exists"))
