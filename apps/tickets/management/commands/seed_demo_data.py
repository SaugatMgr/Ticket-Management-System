from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.tickets.models import (
    MenuLevel1,
    MenuLevel2,
    MenuLevel3,
    Ticket,
    TicketPriority,
    TicketStatus,
)
from apps.users.models import Role

User = get_user_model()


class Command(BaseCommand):
    help = "Seed demo data for menus, tickets, statuses, and priorities"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding menus...")

        level1_dashboard, _ = MenuLevel1.objects.get_or_create(name="Dashboard")
        level1_support, _ = MenuLevel1.objects.get_or_create(name="Support")

        level2_tickets, _ = MenuLevel2.objects.get_or_create(
            parent=level1_support, name="Tickets"
        )
        level2_reports, _ = MenuLevel2.objects.get_or_create(
            parent=level1_support, name="Reports"
        )

        level3_ticket_list, _ = MenuLevel3.objects.get_or_create(
            parent=level2_tickets, name="Ticket List"
        )
        level3_ticket_stats, _ = MenuLevel3.objects.get_or_create(
            parent=level2_reports, name="Ticket Stats"
        )

        self.stdout.write(self.style.SUCCESS("Menus seeded"))

        statuses = [
            ("Open", 1),
            ("In Progress", 2),
            ("Resolved", 3),
            ("Closed", 4),
        ]
        for name, weight in statuses:
            TicketStatus.objects.get_or_create(name=name, weight=weight)
        self.stdout.write(self.style.SUCCESS("Ticket statuses seeded"))

        priorities = [
            ("Low", 1),
            ("Medium", 2),
            ("High", 3),
            ("Critical", 4),
        ]
        for name, weight in priorities:
            TicketPriority.objects.get_or_create(name=name, weight=weight)
        self.stdout.write(self.style.SUCCESS("Ticket priorities seeded"))

        agent_role, _ = Role.objects.get_or_create(name="Support Agent")
        agent, _ = User.objects.get_or_create(
            email="agent@gmail.com",
            defaults={"username": "agent", "role": agent_role},
        )

        customer_role, _ = Role.objects.get_or_create(name="Customer")
        customer, _ = User.objects.get_or_create(
            email="customer@gmail.com",
            defaults={"username": "customer", "role": customer_role},
        )
        self.stdout.write(self.style.SUCCESS("Demo users seeded"))

        open_status = TicketStatus.objects.get(name="Open")
        high_priority = TicketPriority.objects.get(name="High")

        Ticket.objects.get_or_create(
            title="Unable to login",
            description="I cannot login to my account",
            created_by=customer,
            assigned_to=agent,
            menu=level3_ticket_list,
            status=open_status,
            priority=high_priority,
        )

        Ticket.objects.get_or_create(
            title="Bug in checkout process",
            description="Checkout fails when applying coupon",
            created_by=customer,
            assigned_to=agent,
            menu=level3_ticket_stats,
            status=TicketStatus.objects.get(name="In Progress"),
            priority=TicketPriority.objects.get(name="Critical"),
        )
        self.stdout.write(self.style.SUCCESS("Demo tickets seeded"))

        self.stdout.write(self.style.SUCCESS("Demo data seeding complete!"))
