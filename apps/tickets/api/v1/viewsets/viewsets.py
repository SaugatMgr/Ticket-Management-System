from django.db import transaction
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.tickets.api.v1.serializers.serializers import (
    MenuLevel1Serializer,
    MenuLevel2CreateUpdateSerializer,
    MenuLevel2ListDetailSerializer,
    MenuLevel3CreateUpdateSerializer,
    MenuLevel3ListDetailSerializer,
    TicketCreateUpdateSerializer,
    TicketDetailSerializer,
    TicketListSerializer,
    TicketPrioritySerializer,
    TicketStatusSerializer,
)
from apps.tickets.models import (
    MenuLevel1,
    MenuLevel2,
    MenuLevel3,
    Ticket,
    TicketPriority,
    TicketStatus,
)
from utils.pagination import CustomPageSizePagination
from utils.permissions import (
    CanManageTicket,
    CanManageTicketPriority,
    CanManageTicketStatus,
    HasPermission,
)


class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketListSerializer
    action_serializer_mapping = {
        "create": TicketCreateUpdateSerializer,
        "update": TicketCreateUpdateSerializer,
        "partial_update": TicketCreateUpdateSerializer,
        "list": TicketListSerializer,
        "retrieve": TicketDetailSerializer,
    }

    def get_serializer_class(self):
        return self.action_serializer_mapping.get(
            self.action, super().get_serializer_class()
        )

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [CanManageTicket()]
        return [HasPermission()]

    def create(self, request, *args, **kwargs):
        data = request.data
        data["created_by"] = request.user.id

        with transaction.atomic():
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            ticket = serializer.save()
            return Response(data=TicketDetailSerializer(ticket).data)


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


class MenuLevel1ViewSet(ModelViewSet):
    queryset = MenuLevel1.objects.all()
    serializer_class = MenuLevel1Serializer
    pagination_class = CustomPageSizePagination


class MenuLevel2ViewSet(ModelViewSet):
    queryset = MenuLevel2.objects.all()
    pagination_class = CustomPageSizePagination

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return MenuLevel2CreateUpdateSerializer
        return MenuLevel2ListDetailSerializer


class MenuLevel3ViewSet(ModelViewSet):
    queryset = MenuLevel3.objects.all()
    pagination_class = CustomPageSizePagination

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return MenuLevel3CreateUpdateSerializer
        return MenuLevel3ListDetailSerializer
