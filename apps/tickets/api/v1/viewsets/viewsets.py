from rest_framework.viewsets import ModelViewSet

from apps.tickets.api.v1.serializers.serializers import (
    TicketPrioritySerializer,
    TicketSerializer,
    TicketStatusSerializer,
)
from apps.tickets.models import Ticket, TicketPriority, TicketStatus
from utils.permissions import (
    CanManageTicket,
    CanManageTicketPriority,
    CanManageTicketStatus,
    HasPermission,
)


class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [CanManageTicket()]
        return [HasPermission()]


class TicketStatusViewSet(ModelViewSet):
    queryset = TicketStatus.objects.all()
    serializer_class = TicketStatusSerializer
    search_fields = ["name", "weight"]
    filterset_fields = ["name", "weight"]
    ordering_fields = ["name", "weight"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [CanManageTicketStatus()]
        return [HasPermission()]


class TicketPriorityViewSet(ModelViewSet):
    queryset = TicketPriority.objects.all()
    serializer_class = TicketPrioritySerializer
    search_fields = ["name", "weight"]
    filterset_fields = ["name", "weight"]
    ordering_fields = ["name", "weight"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [CanManageTicketPriority()]
        return [HasPermission()]
