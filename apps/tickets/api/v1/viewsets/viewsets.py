from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.notifications.models import NotificationLog
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
from apps.users.models import CustomUser
from utils.constants import NotificationLogActionChoices
from utils.pagination import CustomPageSizePagination
from utils.permissions import RolePermission
from utils.services import get_instance_by_attr


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
    permission_classes = [RolePermission]

    def get_serializer_class(self):
        return self.action_serializer_mapping.get(
            self.action, super().get_serializer_class()
        )

    def create(self, request, *args, **kwargs):
        data = request.data
        data["created_by"] = request.user.id

        with transaction.atomic():
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            ticket = serializer.save()
            return Response(data=TicketDetailSerializer(ticket).data)

    @action(methods=["POST"], detail=True, url_path="assign")
    def assign_ticket(self, request, *args, **kwargs):
        with transaction.atomic():
            content_type = ContentType.objects.get_for_model(Ticket)
            ticket_id = kwargs.get("pk")
            user_id = request.data.get("user_id")

            user = get_instance_by_attr(CustomUser, "id", user_id)
            ticket = get_instance_by_attr(Ticket, "id", ticket_id)

            ticket.assigned_to = user
            ticket.save()

            NotificationLog.objects.create(
                user=user,
                action=NotificationLogActionChoices.ASSIGN,
                content_type=content_type,
                object_id=ticket.id,
                message=f"ticket {ticket.title} assigned to User {user.get_full_name()}.",
            )
            print("**********Ticket Assigned Notification**********")
            print(f"Ticket {ticket.title} assigned to User {user.get_full_name()}.")
            print("**********Ticket Assigned Notification**********")

            return Response({"message": "Ticket assigned successfully."})

    @action(methods=["POST"], detail=True, url_path="unassign")
    def unassign_ticket(self, request, *args, **kwargs):
        with transaction.atomic():
            content_type = ContentType.objects.get_for_model(Ticket)
            ticket_id = kwargs.get("pk")
            user_id = request.data.get("user_id")

            user = get_instance_by_attr(CustomUser, "id", user_id)
            ticket = get_instance_by_attr(Ticket, "id", ticket_id)

            if not ticket.assigned_to or ticket.assigned_to.id != user.id:
                return Response(
                    {"error": "User is not assigned to this ticket."}, status=400
                )

            ticket.assigned_to = None
            ticket.save()

            NotificationLog.objects.create(
                user=user,
                action=NotificationLogActionChoices.UNASSIGN,
                content_type=content_type,
                object_id=ticket.id,
                message=f"Removed User {user.get_full_name()} from Ticket {ticket.title}.",
            )
            print("**********Ticket UnAssigned Notification**********")
            print(f"Removed User {user.get_full_name()} from Ticket {ticket.title}.")
            print("**********Ticket UnAssigned Notification**********")

            return Response({"message": "Ticket unassigned successfully."})


class TicketStatusViewSet(ModelViewSet):
    queryset = TicketStatus.objects.all()
    serializer_class = TicketStatusSerializer
    search_fields = ["name", "weight"]
    filterset_fields = ["name", "weight"]
    ordering_fields = ["name", "weight"]
    permission_classes = [RolePermission]


class TicketPriorityViewSet(ModelViewSet):
    queryset = TicketPriority.objects.all()
    serializer_class = TicketPrioritySerializer
    search_fields = ["name", "weight"]
    filterset_fields = ["name", "weight"]
    ordering_fields = ["name", "weight"]
    permission_classes = [RolePermission]


class MenuLevel1ViewSet(ModelViewSet):
    queryset = MenuLevel1.objects.all()
    serializer_class = MenuLevel1Serializer
    pagination_class = CustomPageSizePagination
    permission_classes = [RolePermission]


class MenuLevel2ViewSet(ModelViewSet):
    queryset = MenuLevel2.objects.all()
    pagination_class = CustomPageSizePagination
    permission_classes = [RolePermission]

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return MenuLevel2CreateUpdateSerializer
        return MenuLevel2ListDetailSerializer


class MenuLevel3ViewSet(ModelViewSet):
    queryset = MenuLevel3.objects.all()
    pagination_class = CustomPageSizePagination
    permission_classes = [RolePermission]

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return MenuLevel3CreateUpdateSerializer
        return MenuLevel3ListDetailSerializer

    @action(methods=["POST"], detail=True, url_path="assign")
    def assign_menu(self, request, *args, **kwargs):
        with transaction.atomic():
            content_type = ContentType.objects.get_for_model(MenuLevel3)
            menu_id = kwargs.get("pk")
            user_id = request.data.get("user_id")

            user = get_instance_by_attr(CustomUser, "id", user_id)
            menu = get_instance_by_attr(MenuLevel3, "id", menu_id)

            user.assigned_menus.add(menu)
            user.save()

            NotificationLog.objects.create(
                user=user,
                action=NotificationLogActionChoices.ASSIGN,
                content_type=content_type,
                object_id=menu.id,
                message=f"Menu {menu.name} assigned to User {user.get_full_name()}.",
            )
            print("**********Menu Assigned Notification**********")
            print(
                f"Added Menu {menu.name} to User {user.get_full_name()} assigned menu list."
            )
            print("**********Menu Assigned Notification**********")

            return Response({"message": "Menu assigned successfully."})

    @action(methods=["POST"], detail=True, url_path="unassign")
    def unassign_menu(self, request, *args, **kwargs):
        with transaction.atomic():
            content_type = ContentType.objects.get_for_model(MenuLevel3)
            menu_id = kwargs.get("pk")
            user_id = request.data.get("user_id")

            user = get_instance_by_attr(CustomUser, "id", user_id)
            menu = get_instance_by_attr(MenuLevel3, "id", menu_id)

            user.assigned_menus.remove(menu)
            user.save()

            NotificationLog.objects.create(
                user=user,
                action=NotificationLogActionChoices.UNASSIGN,
                content_type=content_type,
                object_id=menu.id,
                message=f"Menu {menu.name} unassigned from User {user.get_full_name()} assigned menu list.",
            )

            print("**********Menu Assigned Notification**********")
            print(
                f"Menu {menu.name} unassigned from User {user.get_full_name()} assigned menu list."
            )
            print("**********Menu Assigned Notification**********")

            return Response({"message": "Menu unassigned successfully."})
