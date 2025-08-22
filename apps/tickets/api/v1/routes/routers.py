from rest_framework.routers import DefaultRouter

from apps.tickets.api.v1.viewsets.viewsets import (
    TicketPriorityViewSet,
    TicketStatusViewSet,
    TicketViewSet,
)

ticket_router = DefaultRouter()

ticket_router.register(r"tickets", TicketViewSet, basename="tickets")
ticket_router.register(r"ticket-status", TicketStatusViewSet, basename="ticket-status")
ticket_router.register(
    r"ticket-priority", TicketPriorityViewSet, basename="ticket-priority"
)
