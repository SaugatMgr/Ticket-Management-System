from rest_framework.routers import DefaultRouter

from apps.tickets.api.v1.viewsets.viewsets import (
    MenuLevel1ViewSet,
    MenuLevel2ViewSet,
    MenuLevel3ViewSet,
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
ticket_router.register(r"menu-level-1", MenuLevel1ViewSet, basename="menu-level-1")
ticket_router.register(r"menu-level-2", MenuLevel2ViewSet, basename="menu-level-2")
ticket_router.register(r"menu-level-3", MenuLevel3ViewSet, basename="menu-level-3")
